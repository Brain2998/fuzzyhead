from fuzzyhead import conn, cursor

def divide_dict(dict_path, divide_number, task_id, dict_name):
    content=[]
    with open(dict_path) as f:
        content=f.readlines()
    dict_path_no_x=dict_path[:dict_path.index('.txt')]
    dict_length=len(content)
    part_start_index=0
    part_end_index=divide_number
    dict_exceed=False
    dict_part_id=0
    while True:
        dict_part_name='_'+str(part_start_index)+'-'+str(part_end_index-1)+'.txt'
        with open(dict_path_no_x+dict_part_name, 'w') as f:
            for i in range(part_start_index, part_end_index):
                f.write(content[i])
        conn.execute('INSERT INTO dicts VALUES(?, ?, ?)', (task_id, dict_part_id, dict_name+dict_part_name))
        dict_part_id+=1
        if (dict_exceed):
            break
        part_start_index=part_end_index
        part_end_index=part_end_index+divide_number
        if part_end_index>dict_length:
            part_end_index=dict_length
            dict_exceed=True
    conn.commit()
    
#Tests
#divide_dict('38650-password-sktorrent.txt', 5000)