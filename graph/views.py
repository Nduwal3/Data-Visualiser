import base64
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from  matplotlib import pyplot as plt
from html.parser import HTMLParser
from io import BytesIO
import pandas as pd


csv_dataframe = ''

# Create your views here.
def home(request):
    return render(request , 'index.html')
   
def upload_file(request):
    template = 'index.html'
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name , csv_file)        
        uploaded_file_url = fs.url(filename)        
        return render(request ,template ,  {'data':get_output_data(uploaded_file_url)} )
    else:
        return render(request , template)

def get_output_data(fileurl):
    csv_data_table = create_dataFrame_tohtml(fileurl)
    csv_columns = get_dataframe_columns()
    context= {
        'csv_data_table' : csv_data_table,
        'csv_columns' : csv_columns
    }
    return context

def create_dataFrame_tohtml(url):
    global csv_dataframe
    csv_dataframe = pd.read_csv('.' + url)        
    dataframe_to_html = csv_dataframe.head().to_html()
    return dataframe_to_html        
        
def get_dataframe_columns():
    global csv_dataframe
    columns = csv_dataframe.columns.values
    return columns

def get_x_and_y_columns(request):       
    selected_columns = {
        'x_col_name' : request.POST['x-data'],
        'y_col_name' : request.POST['y-data'],
        'title':request.POST['title'],
        'graph_type' : request.POST['graph-type']
    }
    create_line_graph(selected_columns)    
    return render(request , 'chart.html', {'img_base64': create_image_from_graph()})

def create_line_graph_or_bar(selected_cols):
    global csv_dataframe 
    x_col_data = csv_dataframe[selected_cols['x_col_name']]
    y_col_data = csv_dataframe[selected_cols['y_col_name']]   
    plt.title(selected_cols['title'])
    plt.xlabel(selected_cols['x_col_name'])
    plt.ylabel(selected_cols['y_col_name'])
    plt.bar(x_col_data, y_col_data) 
    plt.grid(True)
    plt.tight_layout()
    # plt.show() 

def create_image_from_graph():
    buffer = BytesIO()
    plt.savefig(buffer , format='png' , dpi = 300)
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
    buffer.close()
    return img_base64

def generate_bar_graph(request):
    global csv_dataframe

    
