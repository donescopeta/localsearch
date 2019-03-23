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

@app.route("/search",methods=['GET', 'POST'])
def search():
    c = mysql.connection.cursor()
    q = request.form.get('q')
    n = request.form.get('n')
    if n == "all" : n = "1e6"
    print(q,n)
    c.callproc("pSzukaj", (q, n ))
    #c.execute("select * from (fileinfo.pSzukaj(%s,%s)) ORDER BY %s ASC ", (q, n, "name"))
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
    
	

@app.route("/")
def index():
	return render_template("index.html")
	
if __name__ == '__main__':
    app.run(host='0.0.0.0')
