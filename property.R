#!/usr/bin/R
library(tidyverse)
library(dplyr)
library(Biostrings)
library(Peptides)

args = commandArgs(T)

inFile = args[1]

print(inFile)
fa <- readAAStringSet(inFile)

table = data.frame(fa) %>%
  rownames_to_column("name") %>%
  mutate("length" = Peptides::lengthpep(seq = fa)) %>% 
  mutate("molecular_weight" = mw(seq = fa)) %>%
  mutate("instability" = instaIndex(seq = fa)) %>%
  mutate("hydrophobicity" = hydrophobicity(seq = fa,scale = "Fauchere")) %>%
  mutate("hydrophobic moment" = hmoment(seq = fa,angle = 100, 
                                        window = nchar(fa))) %>%
  mutate("aliphatic" = aIndex(seq = fa)) %>%     
  mutate("pI" = pI(seq = fa)) %>% 
  mutate("charge" = charge(seq = fa)) %>%
  as_tibble()

table = as.data.frame(table)
table = table[,-2]
colnames(table) = c("names","length","molecular_weight",
                    "instability","hydrophobicity","hydrophobic moment",
                    "aliphatic","pI","charge")


write.csv(table,'/home/ESKtides/static/propert/index.csv',quote = F,row.names = F)
