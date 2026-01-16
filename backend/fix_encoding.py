with open('android_generator.py', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

with open('android_generator_fixed.py', 'w', encoding='utf-8') as out:
    out.write(content)

print('Fixed encoding issues')
