from string import Template

wiki_evaluation_prompt = Template("""
I'm going to give you a wiki page to a gitlab project and the project's README.md file.\n
I want you to tell me if the wiki page is a good representation of the project's README.md file and matches the readme's content.\n
\n
Wiki Page:\n
$wiki
\n
README.md:\n
$readme
\n
If it is a good representation, answer 'yes'. If it is not, answer 'no'. Don't answer anything else.
""")