from mcp.server.fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


@mcp.tool(
    name="read_doc_contents",
    description="Reads the contents of a document and returns it as a string",
)
def read_document(doc_id: str = Field(description="The ID of the document to read.")) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with ID '{doc_id}' not found.")
    return docs[doc_id]


@mcp.tool(
    name="edit_document",
    description="edit a document by replacing a string in the documents content with a new string"
)
def edit_document(
    doc_id: str = Field(description="Id of the document that will be edited"),
    old_str: str = Field(description="The text to replace. Must match exactly, including whitespace"),
    new_str: str = Field(description="The new text to insert in place of the old text")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)


@mcp.tool(
    name="get_all_ids",
    description="returns a list of all document ids"
)
def get_all_ids():
    return docs.keys

@mcp.resource(
    "resource://docs/{doc_id}",
    name="Document Contents",
    description="Returns the contents of a document by ID.",
    mime_type="text/plain",
)
def document_resource(
    doc_id: str = Field(description="The ID of the document to retrieve.")
) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with ID '{doc_id}' not found.")
    return docs[doc_id]

@mcp.prompt(
    name="rewrite_doc_markdown",
    description="Rewrite the contents of a document in well-structured Markdown format.",
)
def rewrite_doc_markdown(
    doc_id: str = Field(description="The ID of the document whose content should be rewritten in Markdown."),
):
    if doc_id not in docs:
        raise ValueError(f"Document with ID '{doc_id}' not found.")

    content = docs[doc_id]
    return [
        {
            "role": "system",
            "content": (
                "You are an expert technical writer. Rewrite the provided document so it is clear, "
                "concise, and formatted as Markdown. Preserve all factual details and organize the "
                "content with appropriate headings, lists, and tables when they improve readability."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Rewrite the following document in Markdown. Use the document ID as the top-level heading "
                f"when helpful.\n\n"
                f"Document ID: {doc_id}\n"
                f"Content:\n{content}"
            ),
        },
    ]


@mcp.prompt(
    name="summarize_doc",
    description="Produce a concise, actionable summary of a document's contents.",
)
def summarize_doc(
    doc_id: str = Field(
        description="The ID of the document whose content should be summarized."
    ),
):
    if doc_id not in docs:
        raise ValueError(f"Document with ID '{doc_id}' not found.")

    content = docs[doc_id]
    return [
        {
            "role": "system",
            "content": (
                "You are a precise analyst. Read the provided document and return a concise summary that "
                "captures the main objective, critical details, and any notable risks or open questions. "
                "Use neutral tone and be brief."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Summarize the following document. Highlight the primary purpose, key points, and any "
                f"important follow-up items.\n\n"
                f"Document ID: {doc_id}\n"
                f"Content:\n{content}"
            ),
        },
    ]


if __name__ == "__main__":
    mcp.run(transport="stdio")
