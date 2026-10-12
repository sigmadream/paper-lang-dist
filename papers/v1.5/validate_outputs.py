import docx
import re

print("=== Checking KSII_TIIS_Paper_v1.5_KO.docx ===")
doc = docx.Document('KSII_TIIS_Paper_v1.5_KO.docx')
print('Paragraphs in KO docx:', len(doc.paragraphs))
print('Tables in KO docx:', len(doc.tables))
for i in [0, 8, 11, 42, 43, 74, 94, 100, 106, 116, 122]:
    p = doc.paragraphs[i]
    has_g = 'graphic' in p._p.xml
    print(f'P{i}: style={p.style.name}, text={p.text[:60]}, has_graphic={has_g}')

for t_idx, table in enumerate(doc.tables):
    print(f'Table {t_idx}: {len(table.rows)} rows, col0={table.rows[0].cells[0].text[:30]}')

print("\n=== Checking KSII_TIIS_Paper_v1.5_KO.md ===")
with open('KSII_TIIS_Paper_v1.5_KO.md', 'r', encoding='utf-8') as f:
    md_text = f.read()

# Check for unicode quotes
unicode_quotes = ['\u201c', '\u201d', '\u2018', '\u2019']
found_uq = [uq for uq in unicode_quotes if uq in md_text]
print('Unicode quotes found:', found_uq)

# Check for bold or italic markdown: ** or __ or *text*
# Notice: asterisks might be used in '*교신저자' or 'k*' or bullets.
# But bold **text** or italic *text* must be checked.
bold_matches = re.findall(r'\*\*.*?\*\*', md_text)
print('Bold ** matches:', len(bold_matches), bold_matches[:5])
under_bold = re.findall(r'__.*?__', md_text)
print('Under bold __ matches:', len(under_bold), under_bold[:5])

# Let's inspect any standalone asterisks
italic_matches = re.findall(r'(?<!\*)\*([^*\s][^*]*[^*\s])\*(?!\*)', md_text)
print('Potential italic * matches:', len(italic_matches), italic_matches[:5])

print('Total lines in MD:', len(md_text.splitlines()))
print('Validation complete.')
