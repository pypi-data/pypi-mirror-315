"""
This is a test file

"""


from wide_analysis import analyze

url = 'https://es.wikipedia.org/wiki/Wikipedia:Consultas_de_borrado/Registro/4_de_junio_de_2008#!Hispahack'
task = "outcome" 

try:
    result = analyze(inp=url, 
                    mode ='url',
                    task='outcome', 
                    openai_access_token='', 
                    explanation=False, 
                    lang='es',
                    platform='wikipedia',
    ) #years='12/2024')


    print("Analysis successful!")
    print(result)
except Exception as e:
    print(f"Error during analysis: {e}")

