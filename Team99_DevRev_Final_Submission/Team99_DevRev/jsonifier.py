def generate_json_schema(cell_value):
    prompt = """Convert the following argument cell value to the general JSON schema. If there are specific fields not present. Ignore them. 
                  general JSON schema (results may be different): 
                  [
                    "tool_name": "tool_name",
                    "arguments": [
                      {
                        "argument_name":"arg_name"
                        "argument_value":"arg_value"
                      }
                    ]
                  ]

                  An example:
                  [
                    {
                      "tool_name": "whoami",
                      "arguments": []
                    },
                    {
                      "tool_name": "works_list",
                      "arguments": [
                        {
                          "argument_name": "issue.priority",
                          "argument_value": ["p0"]
                        },
                        {
                          "argument_name": "owned_by",
                          "argument_value": ["$$PREV[0]"]
                        },
                        {
                          "argument_name": "type",
                          "argument_value": ["issue"]
                        }
                      ]
                    },
                    {
                      "tool_name": "prioritize_objects",
                      "arguments": [
                        {
                          "argument_name": "objects",
                          "argument_value": "$$PREV[1]"
                        }
                      ]
                    },
                    {
                      "tool_name": "get_sprint_id",
                      "arguments": []
                    },
                    {
                      "tool_name": "add_work_items_to_sprint",
                      "arguments": [
                        {
                          "argument_name": "work_ids",
                          "argument_value": "$$PREV[2]"
                        },
                        {
                          "argument_name": "sprint_id",
                          "argument_value": "$$PREV[3]"
                        }
                      ]
                    }
                ]"""
    messages=[{
      "role":"user",
      "content":prompt
  }]

    response=openai.ChatCompletion.create(
      model=model,
      messages=messages,
      temperature=0
  )
    generated_json_schema = response.choices[0].message['content']

    return generated_json_schema

csv_file_path = '/content/resultIB01_base.csv'  
df = pd.read_csv(csv_file_path)

df['generated_json_schema'] = df['arguments'].apply(generate_json_schema)

output_csv_path = 'output_file.csv'
df.to_csv(output_csv_path, index=False)