# ESKtides
The online serve: http://www.phageonehealth.cn:9000/ESKtides<br>
tensorflow: 1.5.0<br>
Keras: 2.2.4

### Some plugins
**1. phy-tree_plugins.rar** is a compressed package of the phylogenetic tree, which contains the html file and static file of the plugin

**2. SCRATCH-1D** download from https://download.igb.uci.edu/, SCRATCH-1D release 1.1

### ESKtides database
ESKtides (ESKAPE derived peptides database): Under the concept of one health, human beings are constantly pursuing a completely new state: the optimal health of people.Antibiotic resistance is one of the biggest threats in global health, food security and development, animals and the environment. Phage lysin is a kind of enzyme synthesized by host bacteria, which has strong host specificity and can hydrolyze the cell wall of bacteria efficiently. The length of antimicrobial peptides is about 6-50 aa, shorter than that of lysin, and easier to be absorbed by the body. In this study, a new antimicrobial peptide mining method based on phage lysins was proposed, we developed a workflow based on phage lysins to mine phage-derived peptide, and used a deep learning model to score bactericidal activity of phage.

![ESKtides](https://github.com/hzaurzli/ESKtides/assets/47686371/f5bd4d96-cca8-4fdf-8045-6b8ba029717b)

Antibiotic resistance is one of the biggest threats in global health, food security and development, antimicrobial peptide(AMPs) possess exceptional structural and functional variety, natural AMPs have been proposed as promising alternatives to traditional antibiotics and as potential next-generation antimicrobial agents (Payel Das et al 2021). ESKAPE is a huge challenge for public health. AMPs mined from the host often have good bactericidal effect on the host. In this study, We mined natural peptides based on ESKAPE peptidoglycan hydrolases based on ESKAPE strains and their phages.

## In ESKtides, users can:

<li>Browse or search ESKAPE strains and phages annotation and filter by user-defined;</li>
<li>Browse or search ESKAPE derived peptides and find out peptides sequences;</li>
<li>Online tools for peptides mining, peptides phylogenetic tree and peptides chemical properties;</li>
<li>Download the ESKtides analysis results of a total of ESKAPE datasets both in strains and phages.</li>
<li>Download page contains the different levels ESKAPE drived peptides in ESKAPE strains and phages.</li>

## Start app
```
python app.py
```
or
```
gunicorn -w 4 -b 0.0.0.0:5000 app:app --timeout 360
```

## Phylogeny
Run /.../.../phylogeny-tree.html in a new session

## Citions
If it is useful for you, please cite https://github.com/hzaurzli/ESKtides/
