{
    'name': 'Supermarket',  #nama modul yg dibaca user di UI
    'version': '1.0',
    'author': 'Jeanny',
    'summary': 'Modul Nilai SIB UK Petra', #deskripsi singkat dari modul
    'description': 'Nilai management module', #bisa nampilkan gambar/ deskripsi dalam bentuk html. html diletakkan
    #di idea/static/description, bisa kasi icon modul juga.
    'category': 'Latihan',
    'website': 'http://sib.petra.ac.id',
    'depends': ['base', 'sales_team', 'membership'],  # list of dependencies, conditioning startup order
    'data': [
        'security/ir.model.access.csv',
        'views/merk_views.xml',
        'views/produk_views.xml',
        'views/members_views.xml',
        'views/penjualan_views.xml',
        'views/jenis_produk_views.xml',
        'views/pembelian_views.xml',
        'views/kategori_produk_views.xml',
        'views/detail_penjualan_views.xml',
    ],
    'qweb':[],  #untuk memberi tahu static file, misal CSS
    'demo': [], #demo data (for unit tests)
    'installable': True,
    'auto_install': False,  # indikasi install, saat buat database baru
}