"""
semantic/pbip_parser.py — Power BI TMDL Parser
================================================
Reads .tmdl files from a PBIP SemanticModel folder and converts
them into LangChain Documents ready for embedding into ChromaDB.

WHAT IS TMDL?
  TMDL (Tabular Model Definition Language) is Microsoft's newer format
  for Power BI semantic models. Instead of one large model.bim JSON file,
  the model is split into multiple readable text files:
    - model.tmdl         → database-level settings
    - relationships.tmdl → all table relationships
    - tables/<name>.tmdl → one file per table (columns + measures)

YOUR FOLDER STRUCTURE:
  project.SemanticModel/
  └── definition/
      ├── model.tmdl
      ├── relationships.tmdl
      └── tables/
          ├── fact_sale.tmdl
          ├── dim_customer.tmdl
          ├── dim_product.tmdl
          ├── dim_date.tmdl
          └── customer_rfm.tmdl

HOW TO POINT THIS PARSER AT YOUR FILES:
  Set TMDL_DEFINITION_PATH in your .env file:
  TMDL_DEFINITION_PATH=C:/Projects/YourReport.SemanticModel/definition

AI CONCEPT — Why we parse the semantic model:
  The RAG system needs to "know" your data model — what tables exist,
  what columns they have, what each DAX measure calculates.
  Without this, the LLM would guess definitions and hallucinate answers.
  By parsing TMDL, we extract this knowledge automatically and store it
  in ChromaDB so the LLM can retrieve the right definition for any question.
"""

import os
import re
from pathlib import Path
from langchain_core.documents import Document




# ── Table name skip list ──────────────────────────────────────────────────────
# These are Power BI internal tables — not part of your actual data model.
# We skip them so they don't pollute the vector store with irrelevant content.
SKIP_TABLES = {
    "DateTableTemplate",
    "LocalDateTable",
    "_LocalDateTable",
}


def _should_skip(table_name: str) -> bool:
    """Return True if this table is a Power BI internal table to ignore."""
    for skip in SKIP_TABLES:
        if table_name.startswith(skip):
            return True
    return False


def parse_table_tmdl(filepath: str) -> Document | None:
    """
    Parse a single table .tmdl file into a LangChain Document.

    Extracts:
      - Table name
      - All column names and data types
      - All DAX measures and their formulas

    RETURNS:
      A Document with plain-English content describing the table,
      or None if the table should be skipped.
    """
    content = Path(filepath).read_text(encoding="utf-8")

    # ── Extract table name ────────────────────────────────────────────────────
    table_match = re.search(r"^table (.+)$", content, re.MULTILINE)
    if not table_match:
        return None

    table_name = table_match.group(1).strip().strip("'")

    if _should_skip(table_name):
        return None

    lines = [f"## Table: {table_name}\n"]

    # ── Extract columns ───────────────────────────────────────────────────────
    # TMDL column pattern:
    #   column ColumnName
    #     dataType: int64
    column_pattern = re.finditer(
        r"^\s+column (.+?)\n(?:.*?\n)*?\s+dataType:\s*(\w+)",
        content,
        re.MULTILINE,
    )

    columns_found = []
    for match in column_pattern:
        col_name = match.group(1).strip().strip("'")
        col_type = match.group(2).strip()
        # Skip Power BI internal columns (start with RowNumber or similar)
        if col_name.startswith("RowNumber") or col_name.startswith("_"):
            continue
        columns_found.append((col_name, col_type))

    if columns_found:
        lines.append("**Columns:**")
        for col_name, col_type in columns_found:
            lines.append(f"- `{col_name}` ({col_type})")
        lines.append("")

    # ── Extract measures ──────────────────────────────────────────────────────
    # TMDL measure pattern:
    #   measure 'Measure Name' = DAX EXPRESSION
    #     formatString: ...
    measure_pattern = re.finditer(
        r"^\s+measure '([^']+)'\s*=\s*(.+?)(?=\n\s+measure|\n\s+column|\n\t\w|\Z)",
        content,
        re.MULTILINE | re.DOTALL,
    )

    measures_found = []
    for match in measure_pattern:
        measure_name = match.group(1).strip()
        # Get just the first line of the expression (the DAX formula)
        expression_raw = match.group(2).strip()
        expression = expression_raw.split("\n")[0].strip()
        measures_found.append((measure_name, expression))

    if measures_found:
        lines.append("**DAX Measures:**")
        for measure_name, expression in measures_found:
            lines.append(f"- `{measure_name}` = {expression}")
        lines.append("")

    return Document(
        page_content="\n".join(lines),
        metadata={
            "source": "tmdl",
            "type": "table",
            "table_name": table_name,
            "file": os.path.basename(filepath),
        }
    )


def parse_measures_as_individual_docs(filepath: str) -> list[Document]:
    """
    Parse each DAX measure in a table file as its OWN separate Document.

    WHY SEPARATE DOCUMENTS?
    If all measures live in one document, a question about 'Gross Margin'
    retrieves the whole table document including irrelevant columns.
    Separating measures means ChromaDB can return just the right measure.

    AI CONCEPT — Chunking strategy:
    How you split content into chunks directly affects retrieval quality.
    One chunk per measure = surgical retrieval.
    One chunk per table = blunt retrieval.
    We do both: one table doc (for schema questions) + one doc per measure
    (for definition questions).
    """
    content = Path(filepath).read_text(encoding="utf-8")

    table_match = re.search(r"^table (.+)$", content, re.MULTILINE)
    if not table_match:
        return []

    table_name = table_match.group(1).strip().strip("'")
    if _should_skip(table_name):
        return []

    measure_pattern = re.finditer(
        r"^\s+measure '([^']+)'\s*=\s*(.+?)(?=\n\s+measure|\n\s+column|\n\t\w|\Z)",
        content,
        re.MULTILINE | re.DOTALL,
    )

    docs = []
    for match in measure_pattern:
        measure_name = match.group(1).strip()
        expression_raw = match.group(2).strip()
        # First line is the DAX formula, rest may include formatString etc.
        formula_lines=[]
        for line in expression_raw.split("\n"):
            stripped = line.strip()
            if stripped.startswith("formatString") or \
                stripped.startswith("displayFolder") or \
                stripped.startswith("annotation") or \
                stripped.startswith("lineageTag") or \
                stripped.startswith("description"):
                break
            formula_lines.append(line)

        formula = "\n".join(formula_lines).strip()

        doc_content = (
            f"## DAX Measure: {measure_name}\n\n"
            f"**Table:** {table_name}\n\n"
            f"**Formula:**\n```dax\n{measure_name} = {formula}\n```\n"
        )

        docs.append(Document(
            page_content=doc_content,
            metadata={
                "source": "tmdl",
                "type": "measure",
                "table_name": table_name,
                "measure_name": measure_name,
            }
        ))

    return docs


def parse_relationships(filepath: str) -> list[Document]:
    """
    Parse relationships.tmdl into a single Document.

    WHY THIS MATTERS:
    When the SQL agent writes a JOIN, it needs to know which columns
    connect which tables. The relationships file gives us that.
    """
    if not os.path.exists(filepath):
        return []

    content = Path(filepath).read_text(encoding="utf-8")

    # TMDL relationship pattern:
    # relationship name
    #   fromTable: TableA
    #   fromColumn: ColumnA
    #   toTable: TableB
    #   toColumn: ColumnB
    rel_blocks = re.findall(
        r"relationship.*?\n"
        r"\s+fromColumn:\s*(.+?)\n"
        r"\s+toColumn:\s*(.+?)\n",
        content,
        re.MULTILINE,
    )

    if not rel_blocks:
        return []

    lines = ["## Table Relationships\n"]
    for  from_col,  to_col in rel_blocks:
        lines.append(
            f"- {from_col.strip() }→ "
            f"{to_col.strip()}"
        )

    return [Document(
        page_content="\n".join(lines),
        metadata={"source": "tmdl", "type": "relationships"}
    )]


def parse_tmdl_to_documents(definition_path: str) -> list[Document]:
    """
    Main entry point. Reads all .tmdl files from the definition/ folder
    and returns a list of LangChain Documents ready for ChromaDB.

    ARGS:
        definition_path: full path to your SemanticModel/definition/ folder

    USAGE (called from ingest.py):
        docs = parse_tmdl_to_documents("C:/Projects/MyReport.SemanticModel/definition")
    """
    definition_path = Path(definition_path)
    tables_path = definition_path / "tables"
    relationships_path = definition_path / "relationships.tmdl"

    if not tables_path.exists():
        raise FileNotFoundError(
            f"tables/ folder not found at: {tables_path}\n"
            f"Check that TMDL_DEFINITION_PATH points to the definition/ folder."
        )

    print(f"📂 Parsing TMDL files from: {definition_path}")

    all_docs = []

    # ── Parse each table file ─────────────────────────────────────────────────
    tmdl_files = sorted(tables_path.glob("*.tmdl"))
    table_count = 0
    measure_count = 0

    for tmdl_file in tmdl_files:
        # Table-level document (schema overview)
        table_doc = parse_table_tmdl(str(tmdl_file))
        if table_doc:
            all_docs.append(table_doc)
            table_count += 1

        # Individual measure documents (one per measure)
        measure_docs = parse_measures_as_individual_docs(str(tmdl_file))
        all_docs.extend(measure_docs)
        measure_count += len(measure_docs)

    # ── Parse relationships ───────────────────────────────────────────────────
    rel_docs = parse_relationships(str(relationships_path))
    all_docs.extend(rel_docs)

    print(f"   ✅ {table_count} tables, {measure_count} measures, {len(rel_docs)} relationship doc")
    return all_docs


def load_markdown_fallback(markdown_path: str) -> list[Document]:
    """
    Fallback: if no TMDL path is configured, load semantic_model.md instead.
    Each ## section becomes one Document (one chunk in ChromaDB).
    """
    if not os.path.exists(markdown_path):
        raise FileNotFoundError(f"Markdown fallback not found at: {markdown_path}")

    content = Path(markdown_path).read_text(encoding="utf-8")
    sections = content.split("\n## ")
    documents = []

    for i, section in enumerate(sections):
        if not section.strip():
            continue
        if i > 0:
            section = "## " + section

        first_line = section.split("\n")[0].strip("# ").strip()
        documents.append(Document(
            page_content=section.strip(),
            metadata={
                "source": "semantic_model_md",
                "type": "markdown_section",
                "section_title": first_line,
            }
        ))

    print(f"   ✅ Loaded {len(documents)} sections from semantic_model.md")
    return documents


if __name__ == "__main__":
    # Quick test — run: python semantic/pbip_parser.py
    # Set your actual path here to test
    import sys
    path = os.getenv("TMDL_DEFINITION_PATH")
    if len(path) > 1:
        docs = parse_tmdl_to_documents(path)
        for doc in docs[:5]:
            print("---")
            print(doc.page_content[:300])
            print("Metadata:", doc.metadata)
    else:
        print("Usage: python semantic/pbip_parser.py <path_to_definition_folder>")
        print("Example: python semantic/pbip_parser.py 'C:/Projects/MyReport.SemanticModel/definition'")