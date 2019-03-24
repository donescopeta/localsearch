from flask import Flask, render_template,render_template_string, request
from flask_mysqldb import MySQL
		
class config:
		MYSQL_HOST="192.168.0.251"
		MYSQL_USER="python"
		MYSQL_PASSWORD="pdf"
		MYSQL_DB="fileinfo"

app = Flask(__name__)
app.config.from_object(config)

mysql =  MySQL(app)

s_url = "http://89.186.9.133:90/pdf/"

@app.route("/rsearch/<q>/<n>")
def search(q,n):
    c = mysql.connection.cursor()
    if n == "all" : n = "1e6"
    c.callproc("pSzukaj", (q, n))
    headers = next(zip(*c.description))[1:]
    rows = c.fetchall()
    
    #return str(rows)
    return render_template_string("""
    <table class="table tableFixHead">
    	<thead><tr>
    		{% for h in ['Name','Title','Subject','Md5'] %}
    			<th>{{ h }}</th>
    		{% endfor %}
    	</tr></thead>
    	<tbody>
			{% for r in rows %}
				<tr>
					<td><a target="_blank" href="{{s_url + r[4] + '/' + r[1]}}" style="display:block; width: 100%; height:100%">{{r[1]}}<a></td>
					{% for h in (2,3,5) %}
						<td>{{ r[h] }}</td>
					{% endfor %}
				</tr>
			{% endfor %}
    	</tbody>
    </table>
    """, headers = headers, rows = rows, s_url = "http://89.186.9.133:90/pdf/")
    	
@app.route("/search/<qu>/")
@app.route("/search/<qu>/<n>")
def u_search(qu,n = "all"):
    return render_template("index.html", q = qu, content = search(qu,n) )

@app.route("/md5/<gmd5>")
def filebymd5(gmd5):
     c = mysql.connection.cursor()
     c.execute("SELECT CONCAT(path,'/',name) FROM pdf WHERE md5 = %s;",(gmd5,))
     return """<meta http-equiv="refresh" content="0; URL='{0}'" />""".format(s_url + c.fetchone()[0])

@app.route("/")
def index():
	return render_template("index.html")
	
if __name__ == '__main__':
    app.run(host='0.0.0.0')
