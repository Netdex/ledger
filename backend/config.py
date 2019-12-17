
config = {
    'db_path':              './ledger-db.json',                             # path to TinyDB database file
    'port':                 5000,                                           # port number when using WSGI
    'devel':                True,                                           # whether to use flask server

    'per_page':             5,

    'upload_folder':        './evidence',
    'allowed_ext':          {'png', 'jpg', 'jpeg', 'gif'},
    'max_content_length':   5 * 1024 * 1024                                 # 5 MB
}