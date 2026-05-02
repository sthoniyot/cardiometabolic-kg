## 6 Conclusion

We have presented NuGeMi-KG, a tri-layer knowledge graph that integrates
nutrigenetics, gut microbiome, and food chemistry under a single
Biolink-aligned schema specifically designed to support cardiometabolic
precision-nutrition research. The resource contains 55,263 nodes and
85,308 edges across eight node types and nine edge types, with 100%
PubMed citation coverage on its literature-derived edges. We defined
fifteen competency questions to evaluate the schema, of which fourteen
return biologically meaningful results, including five tri-layer queries
that surface novel hypothesis-generation patterns — for example, the
convergence of *Streptococcus salivarius*, *Enterococcus faecalis*, and
forty-five cardiometabolic GWAS variants on PPARG. A manual audit of
twenty-four randomly sampled edges places the strict-protocol verification
rate at 62% (95% CI [43, 79]%), with 91% of sampled edges having direct
primary-literature support. The KG, source code, and reproducibility
artefacts are released under CC-BY-4.0 at https://github.com/sthoniyot/cardiometabolic-kg
and archived at Zenodo (DOI to be assigned). NuGeMi-KG is, to our knowledge,
the first publicly available resource in which a single graph query can
traverse food, microbiome, host genetics, and cardiometabolic phenotype in
one statement, and we anticipate that this property will support
hypothesis-generation workflows that have not previously been expressible
against any single public knowledge graph.
