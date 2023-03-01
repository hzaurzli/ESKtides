from flask import Flask, render_template, request
import time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, func
from keras.models import load_model
from numpy import loadtxt, savetxt
import sys,os
from Bio.SeqUtils.ProtParam import ProteinAnalysis


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ESKtides.db'
# app.config['SECRET_KEY'] = 'cairocoders-ednalan'

db = SQLAlchemy(app)

app.jinja_env.variable_start_string = '%%'
app.jinja_env.variable_end_string = '%%'

####################################table
class peptide(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    ORF = db.Column(db.String(200))
    Activity = db.Column(db.Integer)
    Level = db.Column(db.String(200))
    Peptide_ID = db.Column(db.String(200))
    Length = db.Column(db.Integer)
    Type = db.Column(db.String(200))

class genome(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Number = db.Column(db.Integer)
    Accession = db.Column(db.Integer)
    Strains = db.Column(db.String(200))
    Length = db.Column(db.String(200))
    Genome_level = db.Column(db.Integer)
    Type = db.Column(db.String(200))
    ORF_number = db.Column(db.String(200))
    Detail = db.Column(db.String(200))
    Download_faa = db.Column(db.String(200))

class annotate(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Number = db.Column(db.Integer, primary_key=True)
    Locus_tag = db.Column(db.String(200))
    Ftype = db.Column(db.String(200))
    Length = db.Column(db.Integer)
    Gene = db.Column(db.String(200))
    EC_number = db.Column(db.Integer)
    COG = db.Column(db.String(200))
    Product = db.Column(db.String(200))
    Type = db.Column(db.String(200))

#################################### Router
@app.route('/', methods=['get', 'post'])
def home():
    return render_template('home.html')

@app.route('/strains1.html', methods=['get', 'post'])
def strains1():
    return render_template('strains1.html')

@app.route('/peptide.html', methods=['get', 'post'])
def peptide_ajax():
    return render_template('peptide.html')

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
@app.route('/strain_ajax/', methods=['GET', 'POST'])
def strain_ajax():
    param = request.args.to_dict()
    print(param)
    page = param['start']
    strain_type = param['extra_search']
    pageSize = 15
    tag = param['search[value]']
    search = "%{}%".format(tag)
    sortnum = param['order[0][column]']
    dir_sort = param['order[0][dir]']
    selection = param['columns[' + str(sortnum) + '][data]']
    if tag == "":
        if dir_sort == 'desc':
            result_db = genome.query.filter(
                genome.Type.like(strain_type)).order_by(getattr(genome, selection).desc())
            count_num = result_db.count() # 小数据计数的方法
            result = result_db.slice(int(page),int(page)+int(pageSize)).all() # 分页
        else:
            result_db = genome.query.filter(
                genome.Type.like(strain_type)).order_by(getattr(genome, selection).asc())
            count_num = result_db.count() # 小数据计数的方法
            result = result_db.slice(int(page),int(page)+int(pageSize)).all() # 分页
    else:
        if dir_sort == 'desc':
            result_db = genome.query.filter(genome.Type.like(strain_type),
                or_(genome.ID.like(search),
                    genome.Number.like(search),
                    genome.Accession.like(search),
                    genome.Strains.like(search),
                    genome.Length.like(search),
                    genome.Genome_level.like(search),
                    genome.ORF_number.like(search),
                    genome.Detail.like(search),
                    genome.Download_faa.like(search))).order_by(
                getattr(genome, selection).desc())
            count_num = result_db.count() # 小数据计数的方法
            result = result_db.slice(int(page),int(page)+int(pageSize)).all() # 分页

        else:
            result_db = genome.query.filter(genome.Type.like(strain_type),
                or_(genome.ID.like(search),
                    genome.Number.like(search),
                    genome.Accession.like(search),
                    genome.Strains.like(search),
                    genome.Length.like(search),
                    genome.Genome_level.like(search),
                    genome.ORF_number.like(search),
                    genome.Detail.like(search),
                    genome.Download_faa.like(search))).order_by(
                getattr(genome, selection).desc())
            count_num = result_db.count() # 小数据计数的方法
            result = result_db.slice(int(page),int(page)+int(pageSize)).all() # 分页

    alldata = []
    for one in result:
        data = {"ID": one.ID,
                "Number": one.Number,
                "Accession": one.Accession,
                "Strains": one.Strains,
                "Length": one.Length,
                "Genome_level": one.Genome_level,
                "ORF_number": one.ORF_number,
                "Detail": one.Detail,
                "Download_faa": one.Download_faa}
        alldata.append(data)
    rst = {}
    rst["draw"] = param["draw"]
    rst["recordsTotal"] = count_num
    rst["recordsFiltered"] = count_num
    rst["data"] = alldata

    return rst


@app.route('/annotate_ajax/', methods=['GET', 'POST'])
def annotate_ajax():
    param = request.args.to_dict()
    print(param)
    page = param['start']
    strain_type = param['extra_search']
    pageSize = 15
    tag = param['search[value]']
    search = "%{}%".format(tag)
    sortnum = param['order[0][column]']
    dir_sort = param['order[0][dir]']
    selection = param['columns[' + str(sortnum) + '][data]']
    if tag == "":
        if dir_sort == 'desc':
            result_db = annotate.query.filter(
                annotate.Type.like(strain_type)).order_by(getattr(annotate, selection).desc())
            count_num = db.session.query(func.count(annotate.ID)).filter(
                annotate.Type.like(strain_type)).scalar()  # 大数据对表计数的方法
            result = result_db.slice(int(page),int(page)+int(pageSize)).all() # 分页

        else:
            result_db = annotate.query.filter(
                annotate.Type.like(strain_type)).order_by(getattr(annotate, selection).asc())
            count_num = db.session.query(func.count(annotate.ID)).filter(
                annotate.Type.like(strain_type)).scalar() # 大数据对表计数的方法
            result = result_db.slice(int(page),int(page)+int(pageSize)).all() # 分页

    else:
        if dir_sort == 'desc':
            result_db = annotate.query.filter(annotate.Type.like(strain_type),
                or_(annotate.ID.like(search),
                    annotate.Number.like(search),
                    annotate.Locus_tag.like(search),
                    annotate.Ftype.like(search),
                    annotate.Length.like(search),
                    annotate.Gene.like(search),
                    annotate.EC_number.like(search),
                    annotate.COG.like(search),
                    annotate.Product.like(search),
                    annotate.Type.like(search))).order_by(
                getattr(annotate, selection).desc())
            count_num = db.session.query(func.count(annotate.ID)).filter(
                annotate.Type.like(strain_type)).scalar()  # 大数据对表计数的方法
            result = result_db.slice(int(page),int(page)+int(pageSize)).all() # 分页

        else:
            result_db = annotate.query.filter(annotate.Type.like(strain_type),
                  or_(annotate.ID.like(search),
                      annotate.Number.like(search),
                      annotate.Locus_tag.like(search),
                      annotate.Ftype.like(search),
                      annotate.Length.like(search),
                      annotate.Gene.like(search),
                      annotate.EC_number.like(search),
                      annotate.COG.like(search),
                      annotate.Product.like(search),
                      annotate.Type.like(search))).order_by(
                    getattr(annotate, selection).desc())
            count_num = db.session.query(func.count(annotate.ID)).filter(
                annotate.Type.like(strain_type)).scalar()  # 大数据对表计数的方法
            result = result_db.slice(int(page),int(page)+int(pageSize)).all() # 分页

    alldata = []
    for one in result:
        data = {"ID": one.ID,
                "Number": one.Number,
                "Locus_tag": one.Locus_tag,
                "Ftype": one.Ftype,
                "Length": one.Length,
                "Gene": one.Gene,
                "EC_number": one.EC_number,
                "COG": one.COG,
                "Product": one.Product,
                "Type": one.Type}
        alldata.append(data)
    rst = {}
    rst["draw"] = param["draw"]
    rst["recordsTotal"] = count_num
    rst["recordsFiltered"] = count_num
    rst["data"] = alldata

    return rst


@app.route('/tides/', methods=['GET', 'POST'])
def tides():
    param = request.args.to_dict()
    print(param)
    page = param['start']
    strain_type = param['extra_search']
    pageSize = 15
    tag = param['search[value]']
    search = "%{}%".format(tag)
    sortnum = param['order[0][column]']
    dir_sort = param['order[0][dir]']
    selection = param['columns[' + str(sortnum) + '][data]']
    if tag == "":
        if dir_sort == 'desc':
            result_db = peptide.query.filter(
                peptide.Type.like(strain_type)).order_by(getattr(peptide, selection).desc())
            count_num = result_db.count()
            result = result_db.all()[int(page):int(page) + int(pageSize)]
        else:
            result_db = peptide.query.filter(
                peptide.Type.like(strain_type)).order_by(getattr(peptide, selection).asc())
            count_num = result_db.count()
            result = result_db.all()[int(page):int(page) + int(pageSize)]
    else:
        if dir_sort == 'desc':
            result_db = peptide.query.filter(peptide.Type.like(strain_type),
                or_(peptide.ID.like(search),
                    peptide.ORF.like(search),
                    peptide.Activity.like(search),
                    peptide.Level.like(search),
                    peptide.Peptide_ID.like(search),
                    peptide.Length.like(search))).order_by(
                getattr(peptide, selection).desc())
            count_num = result_db.count()
            result = result_db.all()[int(page):int(page) + int(pageSize)]

        else:
            result_db = peptide.query.filter(peptide.Type.like(strain_type),
                or_(peptide.ID.like(search),
                    peptide.ORF.like(search),
                    peptide.Activity.like(search),
                    peptide.Level.like(search),
                    peptide.Peptide_ID.like(search),
                    peptide.Length.like(search))).order_by(
                getattr(peptide, selection).asc())
            count_num = result_db.count()
            result = result_db.all()[int(page):int(page) + int(pageSize)]

    alldata = []
    for one in result:
        data = {"ID": one.ID,
                "ORF": one.ORF,
                "Peptide_ID": one.Peptide_ID,
                "Length": one.Length,
                "Activity": one.Activity,
                "Level": one.Level,}
        alldata.append(data)
    rst = {}
    rst["draw"] = param["draw"]
    rst["recordsTotal"] = count_num
    rst["recordsFiltered"] = count_num
    rst["data"] = alldata

    return rst


@app.route('/up_file/', methods=['GET', 'POST'])  # 接受并存储文件
def up_file():
    if request.method == "POST":
        f = request.files['file']
        print(f.filename)
        f.save('./static/predictdata/' + f.filename)
        time.sleep(3)
        rst = calculation('./static/predictdata/' + f.filename)

        return rst

@app.route('/propert_up_file/', methods=['GET', 'POST'])  # 接受并存储文件
def propert_up_file():
    if request.method == "POST":
        f = request.files['file']
        print(f.filename)
        f.save('./static/propert/' + f.filename)
        time.sleep(3)
        rst = propert('./static/propert/' + f.filename)

        return rst



@app.route('/propert_input_up_file/', methods=['GET', 'POST'])  # 接受并存储文件
def propert_input_up_file():
    if request.method == "GET":
        with open('./static/propert/input.fa','w') as fa:
            data = request.args.get('seq')
            fa.write(data)
        fa.close()

        time.sleep(3)
        rst = propert('./static/propert/input.fa')

        return rst

@app.route('/ajax_test/')
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

def propert(file):
    sequence = ' '
    fasta = {}
    with open(file) as file_one:
        for line in file_one:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                active_sequence_name = line[1:]
                if active_sequence_name not in fasta:
                    fasta[active_sequence_name] = []
                continue
            sequence = line
            fasta[active_sequence_name].append(sequence)

    count = 1
    alldata = []
    path = './static/propert/'
    with open(path + '/propert-json.txt', 'w') as json:
        for key in fasta:
            X = ProteinAnalysis(fasta[key][0])
            mw = "%0.2f" % X.molecular_weight()
            ar = "%0.2f" % X.aromaticity()
            ii = "%0.2f" % X.instability_index()
            ip = "%0.2f" % X.isoelectric_point()
            sec_struc = X.secondary_structure_fraction()
            ss = "%0.2f" % sec_struc[0]
            charge = "%0.2f" % X.charge_at_pH(7)
            print(ss)
            data = {"ID": count, "Peptide": key,
                    "Molecular weight": mw,
                    "Aromaticity": ar, "Instability index": ii,
                    "Isoelectric point": ip, "Charge": charge,
                    "Secondary structure fraction": ss}
            count += 1
            alldata.append(data)
            rst = {}
            rst["data"] = alldata
        json.write(str(rst).replace("'", "\""))  # JSON 格式一定要求双引号
    json.close()
    return rst

if __name__ == "__main__":
    app.run()
