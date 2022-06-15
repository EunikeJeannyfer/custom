{
    'name': 'Multi Discount',  #nama modul yg dibaca user di UI
    'version': '1.0',
    'author': 'Jeanny',
    'summary': 'Modul Inheritance dari Sales Order', #deskripsi singkat dari modul
    'description': 'Ideas management module', #bisa nampilkan gambar/ deskripsi dalam bentuk html. html diletakkan
    #di idea/static/description, bisa kasi icon modul juga.
    'category': 'Latihan',
    'website': 'http://sib.petra.ac.id',
    'depends': ['sale', 'sale_management'],  # list of dependencies, conditioning startup order
                #supaya ketika modul kita diinstal, modul base dan sales team ikut diinstal
    'data': [
        'views/sale_order_views.xml',
    ],
    'qweb':[],  #untuk memberi tahu static file, misal CSS
    'demo': [], #demo data (for unit tests)
    'installable': True,
        #supaya base dan sales team bs install otomatis, installable perlu TRUE
    'auto_install': False,  # indikasi install, saat buat database baru
}
