import cgi
form = cgi.FieldStorage()

title = form.getvalue('title')
first_name_tutor = form.getvalue('first_name_tutor')
last_name_tutor  = form.getvalue('last_name__tutor')
first_name_kid = form.getvalue('first_name_kid')
last_name_kid  = form.getvalue('last_name__kid')
date = form.getvalue('date')
formula = form.getvalue('formula')
amount = form.getvalue('amount')
comment = form.getvalue('comment')
print("Content-type:text/html")
print("Hello - Second CGI Program")
print("(first_name, last_name)")

f = open("/files/myfile.txt", "x")
f.write("Agregando Contenido")
f.close()