from flask import Flask, render_template, request
import time
from keras.models import load_model
from numpy import loadtxt, savetxt
import sys,os
from Bio.SeqUtils.ProtParam import ProteinAnalysis


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
# # app.config['SECRET_KEY'] = 'cairocoders-ednalan'
#
# db = SQLAlchemy(app)

app.jinja_env.variable_start_string = '%%'
app.jinja_env.variable_end_string = '%%'

#################################### Router
@app.route('/', methods=['get', 'post'])
def home():
    return render_template('home.html')

@app.route('/strains1.html', methods=['get', 'post'])
def strains1():
    return render_template('strains1.html')

@app.route('/predict.html', methods=['get', 'post'])
def predict():
    return render_template('predict.html')

@app.route('/phylotree.html', methods=['get', 'post'])
def phylotree():
    return render_template('phylotree.html')


@app.route('/phylo.html', methods=['get', 'post'])
def phylo():
    return render_template('phylo.html')

@app.route('/property.html', methods=['get', 'post'])
def property():
    return render_template('property.html')

@app.route('/statistics.html', methods=['get', 'post'])
def statistics():
    return render_template('statistics.html')

@app.route('/download.html', methods=['get', 'post'])
def download():
    return render_template('download.html')

@app.route('/help.html', methods=['get', 'post'])
def help():
    return render_template('help.html')

#########################################ajax
@app.route('/up_file/', methods=['GET', 'POST'])  # 接受并存储文件
def up_file():
    if request.method == "POST":
        f = request.files['file']
        print(f.filename)
        f.save('./static/predictdata/' + f.filename)
        time.sleep(3)
        rst = calculation('./static/predictdata/' + f.filename)

        return rst


@app.route('/ajax/')
def ajax():
    rst =  {"data":[
        { "ID": 0, "ORF": "c","Activity":10,"Level":"high","Strains":"asa","Detail":"ll"},
        { "ID": 1, "ORF": "c","Activity":10,"Level":"high","Strains":"asa","Detail":"ll"},
        { "ID": 2, "ORF": "c","Activity":10,"Level":"high","Strains":"asa","Detail":"ll"},
        { "ID": 3, "ORF": "c","Activity":10,"Level":"high","Strains":"asa","Detail":"ll"}
    ]}

    return rst


@app.route('/detail/<Strains>')
def detail(Strains):
    return render_template('strains2.html')

###############################################cal
def calculation(fasta):
    path = './static/predictdata'

    os.system(r".\static\tools\perl\bin\perl.exe .\static\tools\perl\format.pl %s none > %s"
             % (fasta, path + '/tmp.txt'))
    time.sleep(5)

    model = load_model('./static/tools/Activity/lstm.h5')
    x = loadtxt(path + '/tmp.txt', delimiter=",")
    preds = model.predict(x)
    savetxt(path + '/tmpActivity.txt', preds, fmt="%.8f", delimiter=",")

    with open(fasta) as fa:
        fa_dict = {}
        for line in fa:
            line = line.replace('\n', '')
            if line.startswith('>'):
                seq_name = line[1:]
                fa_dict[seq_name] = ''
            else:
                fa_dict[seq_name] += line.replace('\n', '')
    fa.close()

    lis = []
    with open(path + '/tmpActivity.txt') as ac:
        for i in ac:
            i = i.replace('\n', '')
            lis.append(i)
    ac.close()

    for i_1 in range(0, len(lis)):
        key = list(fa_dict.keys())[i_1]
        val = [fa_dict.get(key, [])] + [lis[i_1]]
        fa_dict[key] = val

    with open(path + '/result-act.txt', 'w') as f:
        for key in fa_dict:
            lines = key + '\t' + fa_dict[key][0] + '\t' + fa_dict[key][1] + '\n'
            print(lines)
            f.write(lines)
    f.close()

    os.remove(path + '/tmp.txt')
    os.remove(path + '/tmpActivity.txt')

    count = 1
    alldata = []
    with open(path + '/result-act-json.txt','w') as json:
        with open(path + '/result-act.txt') as r:
            for one in r:
                one = one.strip().split('\t')
                if float(one[2]) >= 0.5:
                    data = {"ID": count, "ORF": one[0], "Sequence": one[1],
                            "Score": one[2]}
                    count += 1
                    alldata.append(data)
                    rst = {}
                    rst["data"] = alldata
        r.close()
        json.write(str(rst).replace("'","\"")) # JSON 格式一对要求双引号
    json.close()
    return rst



if __name__ == "__main__":
    app.run()
