# ESKtides
ESKtides database
ESKtides (ESKAPE derived peptides database): Under the concept of one health, human beings are constantly pursuing a completely new state: the optimal health of people.Antibiotic resistance is one of the biggest threats in global health, food security and development, animals and the environment. Phage lysin is a kind of enzyme synthesized by host bacteria, which has strong host specificity and can hydrolyze the cell wall of bacteria efficiently. The length of antimicrobial peptides is about 6-50 aa, shorter than that of lysin, and easier to be absorbed by the body. In this study, a new antimicrobial peptide mining method based on phage lysins was proposed, we developed a workflow based on phage lysins to mine phage-derived peptide, and used a deep learning model to score bactericidal activity of phage.

![ESKtides](https://user-images.githubusercontent.com/47686371/225228138-a6b4aa54-c40a-4c03-8916-5f6601c30c75.png)

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
Run ../static/phylogeny.html in a new session
