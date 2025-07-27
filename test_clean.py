import re

def clean_response_text(text):
    if not isinstance(text, str):
        return str(text)
    
    # Remove common markdown wrappers
    text = text.strip()
    
    # Remove **Result:** prefix
    if text.startswith('**Result:**'):
        text = text.replace('**Result:**', '').strip()
    
    # Remove markdown code blocks
    if text.startswith('```') and text.endswith('```'):
        text = text[3:-3].strip()
    
    # Remove any remaining ```
    while text.startswith('```'):
        text = text[3:].strip()
    while text.endswith('```'):
        text = text[:-3].strip()
    
    # Split into lines and clean up explanation sections
    lines = text.split('\n')
    final_lines = []
    
    for line in lines:
        line_stripped = line.strip()
        # Stop processing when we hit explanation patterns
        if (line_stripped.startswith('Explanation:') or 
            line_stripped == 'Explanation:' or
            line_stripped.startswith('I invoked') or
            line_stripped.startswith('The agent returned')):
            break  # Stop here - don't include this line or anything after
        final_lines.append(line)
    
    # Join back and clean up extra whitespace
    cleaned_text = '\n'.join(final_lines).strip()
    
    # Remove multiple consecutive newlines
    cleaned_text = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned_text)
    
    # Final cleanup for any remaining ```
    cleaned_text = re.sub(r'```\s*$', '', cleaned_text).strip()
    cleaned_text = re.sub(r'```', '', cleaned_text).strip()
    
    return cleaned_text

# Test with the story response that still shows Explanation
test_text = """Title: The Little Seed's Big Journey
Story: Once upon a time, in a small village nestled among green fields, lived a tiny seed. This seed was smaller than a grain of rice but dreamed of becoming a big, strong tree. One sunny morning, a farmer gently placed the seed in the soil. The seed felt dark and lonely at first. Then, the rain came. Drops of water seeped into the soil, and the seed felt a little tickle.

"I think it's time," whispered the seed to itself. Slowly, it pushed a tiny root down into the earth and a little sprout up towards the sky. The sun warmed its little leaves, and the rain quenched its thirst. Days turned into weeks, and the little sprout grew taller. It became a small plant with many leaves. Children in the village would come and water it, singing songs.

One day, a cow came and tried to eat the little plant! But the children shooed the cow away and built a small fence around the plant to protect it. The plant continued to grow, stronger and taller each day. It grew branches that reached out like arms, offering shade to anyone who needed it. Birds built nests in its branches, and squirrels played hide-and-seek around its trunk.

Years passed, and the little seed had become a big, strong tree. The tree gave fruits to the villagers and provided shelter from the hot sun and heavy rains. The children, now grown up, brought their own children to play under its shade. The tree stood tall and proud, watching over the village, happy to be a part of their lives.

Takeaway: Even the smallest of us can grow to be strong and helpful with a little care and patience.

Explanation:"""

print('Testing with story response...')
cleaned = clean_response_text(test_text)
print('CLEANED OUTPUT:')
print('=' * 60)
print(cleaned)
print('=' * 60)

# Check if Explanation is removed
if 'Explanation:' in cleaned:
    print('❌ STILL HAS EXPLANATION - function not working properly')
    print('Found at position:', cleaned.find('Explanation:'))
else:
    print('✅ EXPLANATION REMOVED - function working correctly')
