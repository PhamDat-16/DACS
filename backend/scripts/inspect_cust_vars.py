import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

cust_start = content.find('CUSTOMER PORTAL SCREENS')
modals_start = content.find('CUSTOMER MODALS')
app_end = content.find('<!-- Vue 3 Application Script -->')
cust_section = content[cust_start:app_end] if cust_start != -1 else ''

v_ifs = set(re.findall(r'v-if="([^"]+)"', cust_section))
v_models = set(re.findall(r'v-model="([^"]+)"', cust_section))
clicks = set(re.findall(r'@click="([^"]+)"', cust_section))

print("=== V-IFS ===")
for x in sorted(v_ifs):
    print(x)

print("\n=== V-MODELS ===")
for x in sorted(v_models):
    print(x)

print("\n=== CLICKS ===")
for x in sorted(clicks):
    print(x)
