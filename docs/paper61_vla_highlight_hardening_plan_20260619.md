# Paper 61 VLA Highlight Hardening Plan

Objective: make Paper 61's boxed PDF highlights match the VLA-v4 role-model PDF while preserving the frozen WAM Contact Counterfactuals evidence and STRONG_REVISE scientific conclusion.

## Role-Model Target

- Citation links use green rectangular borders with no fill.
- Internal references use red rectangular borders with no fill.
- URL links use the same green border family as citations.
- Border width is `pdfborder={0 0 1}`, matching the VLA-v4 annotation metadata.
- Boxes remain tight to linked text and must not affect typography, line spacing, table layout, figure captions, or scientific content.

## Current Paper 61 Mismatch

- `Downloads/61.pdf` has orange citation boxes on pages 1, 2, and 6.
- `Downloads/61.pdf` has a blue internal-reference box on page 6.
- `Downloads/61.pdf` has darker green URL boxes on pages 24 and 25.
- All link boxes currently use border width `1.35`, visibly heavier than the VLA-v4 role model.
- The source cause is `paper/main.tex`, where `pdfborder`, `citebordercolor`, `linkbordercolor`, and `urlbordercolor` diverge from the VLA-v4 target.

## Execution Plan

1. Keep RAM use low by rendering only affected pages before and after the edit: pages 1, 2, 6, 24, and 25.
2. Change only the `hyperref` style in `paper/main.tex`:
   - `pdfborder={0 0 1}`
   - `citebordercolor={0 1 0}`
   - `linkbordercolor={1 0 0}`
   - `urlbordercolor={0 1 0}`
3. Rebuild with the existing repository build script so `paper/main.pdf` and `C:\Users\wangz\Downloads\61.pdf` stay aligned.
4. Validate the rebuilt PDF annotation metadata with `pypdf`.
5. Render pages 1, 2, 6, 24, and 25 again and visually compare with the VLA-v4 role model.
6. Update README/status wording to record VLA-v4 link-box styling.
7. Remove Paper 61 temporary render folders, then commit and push the clean repo.

## Non-Goals

- Do not rerun MuJoCo experiments.
- Do not change result tables, figures, acceptance decision, or STRONG_REVISE scientific conclusion.
- Do not pad page count or alter paper scope for this visual hardening pass.
