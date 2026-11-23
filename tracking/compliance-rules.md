# Compliance Rules

This document defines the five compliance rules (CR-1 through CR-5) applied to every camera-ready paper before its **Compliance Check** column in `paper-tracking.md` can be set to `Pass`. A paper must pass **all five rules**; a single failure yields `Fail`.

---

## CR-1 — Page Count

**Rule:** The camera-ready paper must meet Springer LNCS minimum length requirements (CS Editors Proceedings Guidelines, Sect. 3.4) and stay at or below the **20-page** soft limit, including all content (body, references, appendices, Disclosure of Interests section, and any acknowledgements).

**Applying CR-1:**

| Page count | Action |
|------------|--------|
| < 4 pages | **CR-1 fails.** Springer moves papers shorter than 4 pages to the back matter and does **not** index them on Springer Nature Link. Contact the authors to expand to ≥ 4 pages (especially verify Paper #2, Sub. ID `3744`, Extended Abstract). |
| 4–5 pages | Only acceptable for poster/extended-abstract formats after confirming with Springer (Sect. 3.4). |
| 6–11 pages | Acceptable for short papers (≥ 6 pages). Note: across the volume, **at least two thirds of published papers must be full papers (≥ 12 pages)**. |
| 12–20 pages | Full paper — CR-1 passes. |
| 21–~22 pages | Flag the paper. Contact the authors and request a reduction. Do not automatically reject; use editorial judgement. CR-1 remains `Pending` until resolved. |
| ≥ 30 pages | Do not accept without first contacting **anna.kramer@springer.com**. Springer must approve any paper at or above 30 pages before it can be included in the volume. |

---

## CR-2 — LNCS Formatting

**Rule:** Authors must have used the official LNCS template throughout.

- **LaTeX:** paper must use `llncs.cls` (Springer LNCS LaTeX class). Check the `\documentclass` declaration.
- **Word:** paper must use the official LNCS Word template (`.docx`). Files submitted as `.docm` (macro-enabled Word document) are **not acceptable**; authors must resave as `.docx` before the submission can be accepted.

**Applying CR-2:**

1. For LaTeX submissions, open the main `.tex` file and confirm `\documentclass{llncs}` (or equivalent with the `llncs.cls` class file present).
2. For Word submissions, confirm the file extension is `.docx`, not `.docm`.
3. Visually check the PDF for LNCS-style header fonts, margins, and reference style as a secondary indicator.

---

## CR-3 — Author List Consistency

**Rule:** The author names listed in the **paper header** (PDF first page and, for LaTeX, the `\author{}` command) must match the **Authors** field in `paper-tracking.md` exactly — same names, same order, same spelling.

**Applying CR-3:**

1. Open the camera-ready PDF and read the author list from the paper header.
2. Compare against the Authors column in `paper-tracking.md` for the same paper row.
3. Any discrepancy (added, removed, reordered, or differently spelled name) requires author confirmation in writing before the entry can be corrected and CR-3 cleared.
4. For authors contributing to more than one paper, confirm their name is spelled and structured identically across all papers and `submission/toc.csv` (Springer Guidelines Sect. 5.3).
5. Flag any non-straightforward, multi-part, or possibly reversed author names (e.g., verify `Lefevre Louis` in Paper #6, Sub. ID `4854`) for the Author Index disambiguation list (`Given Name; Family Name`) sent to Springer.
6. Confirm compliance with Springer's policy (Sect. 3) that no PC Chair, PC member, or volume editor co-authors more than **2 papers** in the volume.

> **Note:** Do not silently update the Tracking Table to match the paper. Discrepancies may indicate a co-author was removed or added after acceptance, which must be cleared with the program chairs. Once files are sent to Springer, authorship cannot be changed.

---

## CR-4 — LTP Corresponding Author Consistency

**Rule:** The corresponding author named on the signed **Licence-to-Publish (LTP)** agreement must be the same person marked as corresponding author in the **paper header**. Only the LNCS-specific LTP form is valid; no other Springer agreement applies.

Additional constraints:

- **Wet (physical, non-digital) signature is required.** Scanned handwritten signatures on a printed form are acceptable. Electronically applied or typed signatures are not.
- Only **one** corresponding author is allowed per paper.

**Applying CR-4:**

1. Confirm the LTP form is the LNCS-specific version (not a generic Springer or open-access form).
2. Read the corresponding author name from the signed LTP.
3. Read the corresponding author name from the paper header (look for a footnote marker, an email address, or an explicit "corresponding author" annotation).
4. Confirm the two names match.
5. Confirm the signature is handwritten (wet); reject digital signatures and request a re-signed form.

---

## CR-5 — Disclosure of Interests Section

**Rule:** Every paper must include a **"Disclosure of Interests"** section. Springer mandates this section for all LNCS proceedings papers.

Required placement and formatting:

- Rendered as a **third-level heading** (e.g., `\subsubsection*{Disclosure of Interests}` in LaTeX, or `### Disclosure of Interests` in Markdown/Word).
- Placed **after** any Acknowledgments section.
- Placed **before** the reference list.

**Applying CR-5:**

1. Scroll to the end of the paper body (before the references) and confirm the "Disclosure of Interests" heading is present.
2. Check that it appears after Acknowledgments (if present).
3. The section may contain "The authors have no competing interests to declare" or similar — any substantive content is acceptable as long as the section heading is present.

---

## Applying the Check

Work through CR-1 to CR-5 in order for each paper. Use the checklist below:

```
Paper #__  Sub. ID: ______

[ ] CR-1  Page count ≥ 4 (full ≥ 12, short ≥ 6, ≥ 2/3 full overall) and ≤ 20 soft limit (or action noted)
[ ] CR-2  LNCS LaTeX llncs.cls or .docx Word template used; no .docm files
[ ] CR-3  Author list matches Tracking Table exactly; consistent across papers; complex names flagged for Author Index; PC 2-paper cap respected
[ ] CR-4  LTP is LNCS-specific form; corresponding author matches paper header; wet signature present
[ ] CR-5  "Disclosure of Interests" section present, correctly placed (after Acknowledgments, before references)
```

A paper reaches `Pass` only when **all five boxes are checked**. If any rule fails, the overall result is `Fail`.

---

## Recording Results

Update `tracking/paper-tracking.md` immediately after completing the check for each paper.

| Outcome | Compliance Check value | Additional action |
|---------|------------------------|-------------------|
| All five rules pass | `Pass` | No further action needed. |
| Any rule fails | `Fail` | Add a blockquote failure note on the line immediately below the paper's row (see format below). Return the paper to the authors with specific instructions. |
| Check not yet started | `Pending` | Default; leave unchanged until check is complete. |

**Failure note format:**

```
> **Failure note (#N):** CR-X: <brief description of the failure and date returned to authors>.
```

For example:

```
> **Failure note (#7):** CR-1: Paper is 22 pages (exceeds 20-page soft limit). Authors contacted 2026-04-16 and asked to reduce to ≤ 20 pages.
```

If multiple rules fail, list each on a separate line within the same blockquote:

```
> **Failure note (#12):** CR-2: Submitted as .docm file; authors asked to resave as .docx.  
> CR-5: "Disclosure of Interests" section missing; authors asked to add it before references.
```

Once a resubmission arrives, reset the Compliance Check column to `Pending` and re-run all five checks from CR-1.
