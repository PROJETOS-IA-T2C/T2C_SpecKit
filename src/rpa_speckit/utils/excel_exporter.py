import openpyxl
import json
import sys
import os
from copy import copy

def find_footer_row(ws, start_row, search_col=2):
    """Procura a linha onde começa o rodapé (texto não vazio que não é task)."""
    for row in range(start_row, start_row + 500):
        cell_val = ws.cell(row=row, column=search_col).value
        cell_val_c = ws.cell(row=row, column=search_col+1).value
        text = str(cell_val) if cell_val else ""
        text_c = str(cell_val_c) if cell_val_c else ""
        
        if "Saída do processo" in text or "Saída do processo" in text_c:
            return row
    return None

def copy_style(source_cell, target_cell):
    """Copia estilo de uma célula para outra."""
    if source_cell.has_style:
        if source_cell.font: target_cell.font = copy(source_cell.font)
        if source_cell.border: target_cell.border = copy(source_cell.border)
        if source_cell.fill: target_cell.fill = copy(source_cell.fill)
        if source_cell.number_format: target_cell.number_format = copy(source_cell.number_format)
        if source_cell.alignment: target_cell.alignment = copy(source_cell.alignment)
        if source_cell.protection: target_cell.protection = copy(source_cell.protection)

def export_to_excel(tasks_data, template_path, output_path, process_name="Processo RPA"):
    """
    Preenche o template Excel com os dados fornecidos.
    
    Args:
        tasks_data (list): Lista de dicts com chaves 'robot', 'name', 'description', 'estimate'.
        template_path (str): Caminho do arquivo .xlsx template.
        output_path (str): Caminho onde salvar o arquivo final.
        process_name (str): Nome do processo para preencher no cabeçalho.
    """
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template não encontrado: {template_path}")

    print(f"Carregando template: {template_path}")
    wb = openpyxl.load_workbook(template_path)
    ws = wb.active

    START_ROW = 12
    COL_BOT = 2
    COL_ACTIVITY = 3
    COL_TIME = 4

    # 1. Encontrar Footer
    footer_row = find_footer_row(ws, START_ROW)
    
    if not footer_row:
        print("⚠️ Rodapé não encontrado. Usando append simples.")
        footer_row = START_ROW + len(tasks_data) + 10

    available_rows = footer_row - START_ROW
    needed_rows = len(tasks_data)
    
    # 2. Ajustar Linhas (Inserir ou Deletar)
    if needed_rows > available_rows:
        rows_to_insert = needed_rows - available_rows
        print(f"Inserindo {rows_to_insert} linhas...")
        ws.insert_rows(footer_row, amount=rows_to_insert)
        
        # Copiar estilo da linha anterior
        ref_row = footer_row - 1
        for i in range(rows_to_insert):
            target_row = footer_row + i
            for col in range(1, 10):
                copy_style(ws.cell(ref_row, col), ws.cell(target_row, col))
                
    elif needed_rows < available_rows:
        rows_to_delete = available_rows - needed_rows
        if rows_to_delete > 0:
            print(f"Deletando {rows_to_delete} linhas excedentes...")
            delete_start = START_ROW + needed_rows
            ws.delete_rows(delete_start, amount=rows_to_delete)

    # 3. Preencher Cabeçalho
    ws["C6"] = process_name

    # 4. Preencher Tasks
    current_row = START_ROW
    for task in tasks_data:
        # Coluna B: Robô
        cell_bot = ws.cell(row=current_row, column=COL_BOT)
        if not isinstance(cell_bot, openpyxl.cell.cell.MergedCell):
            cell_bot.value = task.get('robot', '')

        # Coluna C: Atividade
        activity_text = f"{task.get('name', '')}\n{task.get('description', '')}"
        cell_act = ws.cell(row=current_row, column=COL_ACTIVITY)
        
        # Tratamento Merge
        if isinstance(cell_act, openpyxl.cell.cell.MergedCell):
             for rng in ws.merged_cells.ranges:
                 if cell_act.coordinate in rng:
                     ws.cell(row=rng.min_row, column=rng.min_col).value = activity_text
                     break
        else:
            cell_act.value = activity_text
            cell_act.alignment = openpyxl.styles.Alignment(wrap_text=True, vertical='top')

        # Coluna D: Estimativa
        cell_time = ws.cell(row=current_row, column=COL_TIME)
        if not isinstance(cell_time, openpyxl.cell.cell.MergedCell):
             # Tenta converter para float
             try:
                 val = float(task.get('estimate', 0))
             except:
                 val = task.get('estimate', 0)
             cell_time.value = val

        current_row += 1

    wb.save(output_path)
    try:
        print(f"Arquivo salvo: {os.path.abspath(output_path)}")
    except UnicodeEncodeError:
        print(f"Arquivo salvo: {os.path.abspath(output_path)}".encode('utf-8', errors='ignore').decode('utf-8'))

if __name__ == "__main__":
    # Modo CLI: Recebe JSON via argumento ou stdin
    # Exemplo uso: python excel_exporter.py '{"tasks": [...], "template": "...", "output": "..."}'
    if len(sys.argv) > 1:
        try:
            # Se o argumento for um arquivo json
            if sys.argv[1].endswith('.json') and os.path.exists(sys.argv[1]):
                with open(sys.argv[1], 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                # Tenta parsear string json direta
                data = json.loads(sys.argv[1])
            
            export_to_excel(
                data['tasks'], 
                data['template'], 
                data['output'],
                data.get('process_name', 'Processo RPA')
            )
        except Exception as e:
            print(f"Erro ao processar argumentos: {e}")
            sys.exit(1)
    else:
        print("Uso: python excel_exporter.py '<json_data>'")

