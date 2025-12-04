import re
import sys


arXivcats = set([
        "q-fin.PM", "math.OC", "q-bio.TO", "math.CT", "q-bio.PE", "q-bio.BM",
        "math.KT", "nlin.CD", "q-fin.TR", "econ.EM", "math.SG", "cs.IT",
        "math.PR", "cs.DB", "eess.IV", "cs.NI", "cs.DC", "math.NA", "math.CA",
        "math.AP", "astro-ph.IM", "cs.IR", "nlin.CG", "eess.SY", "stat.TH",
        "math.LO", "q-bio.SC", "math.CV", "cs.ET", "astro-ph.SR", "cs.RO",
        "q-fin.CP", "cs.GL", "q-fin.ST", "q-fin.MF", "econ.TH", "q-bio.NC",
        "cs.CR", "math.CO", "cs.AR", "math.QA", "math.HO", "math.GT", "math.MP",
        "cs.DL", "nlin.PS", "cs.GT", "math.RT", "cs.MM", "math.NT", "cs.CV",
        "cs.NA", "math.SP", "q-bio.GN", "cs.CL", "cs.AI", "nlin.AO", "math.ST",
        "cs.LG", "cs.GR", "math.AT", "stat.ME", "math.GR", "math.IT", "q-fin.PR",
        "astro-ph.GA", "cs.SI", "cs.CY", "stat.ML", "cs.OS", "cs.SC", "math.MG",
        "math.OA", "cs.MS", "cs.MA", "cs.PF", "stat.AP", "eess.SP", "math.GN",
        "nlin.SI", "stat.CO", "eess.AS", "q-bio.OT", "cs.LO", "math.GM", "cs.CE",
        "astro-ph.EP", "cs.NE", "q-fin.RM", "astro-ph.CO", "stat.OT", "math.DG",
        "math.AG", "math.FA", "math.DS", "math.AC", "cs.PL", "q-bio.QM", "q-bio.MN",
        "q-fin.EC", "cs.SY", "cs.HC", "astro-ph.HE", "econ.GN", "cs.OH", "math.RA",
        "cs.CC", "cs.DS", "cs.SD", "cs.SE", "q-bio.CB", "q-fin.GN", "cs.DM", "cs.CG",
        "cs.FL", "cond-mat.dis-nn", "cond-mat.mes-hall", "cond-mat.mtrl-sci",
        "cond-mat.other", "cond-mat.quant-gas", "cond-mat.soft", "cond-mat.stat-mech",
        "cond-mat.str-el", "cond-mat.supr-con", "gr-qc", "hep-ex", "hep-lat", "hep-ph",
        "hep-th", "math-ph", "nucl-ex", "nucl-th", "physics.acc-ph", "physics.ao-ph",
        "physics.app-ph", "physics.atm-clus", "physics.bio-ph", "physics.atom-ph",
        "physics.chem-ph", "physics.class-ph", "physics.comp-ph", "physics.data-an",
        "physics.ed-ph", "physics.flu-dyn", "physics.gen-ph", "physics.geo-ph",
        "physics.hist-ph", "physics.ins-det", "physics.med-ph", "physics.optics",
        "physics.plasm-ph", "physics.pop-ph", "physics.soc-ph", "physics.space-ph",
        "quant-ph"
    ])




def extract(hugestring:str)->set:
    
    pattern = r'(?<=\s)[a-zA-Z-]+\.[A-Z]{2}'
    categories = re.findall(pattern, hugestring)
    return set(categories)


def main():
    # with open(sys.argv[1]) as f:
    #     hugestring = f.read()
    # categories = extract(hugestring)
    # print("[", end="")
    # print(", ".join(categories), end="")  # nicer, no trailing comma
    # print("]")
    # print("[",end = "")
    # for i in sdfcategories:
    #     print('"',i,'"',",",end="")
    # print("]")

    
    # categories = [
    #     "q-fin.PM", "math.OC", "q-bio.TO", "math.CT", "q-bio.PE", "q-bio.BM",
    #     "math.KT", "nlin.CD", "q-fin.TR", "econ.EM", "math.SG", "cs.IT",
    #     "math.PR", "cs.DB", "eess.IV", "cs.NI", "cs.DC", "math.NA", "math.CA",
    #     "math.AP", "astro-ph.IM", "cs.IR", "nlin.CG", "eess.SY", "stat.TH",
    #     "math.LO", "q-bio.SC", "math.CV", "cs.ET", "astro-ph.SR", "cs.RO",
    #     "q-fin.CP", "cs.GL", "q-fin.ST", "q-fin.MF", "econ.TH", "q-bio.NC",
    #     "cs.CR", "math.CO", "cs.AR", "math.QA", "math.HO", "math.GT", "math.MP",
    #     "cs.DL", "nlin.PS", "cs.GT", "math.RT", "cs.MM", "math.NT", "cs.CV",
    #     "cs.NA", "math.SP", "q-bio.GN", "cs.CL", "cs.AI", "nlin.AO", "math.ST",
    #     "cs.LG", "cs.GR", "math.AT", "stat.ME", "math.GR", "math.IT", "q-fin.PR",
    #     "astro-ph.GA", "cs.SI", "cs.CY", "stat.ML", "cs.OS", "cs.SC", "math.MG",
    #     "math.OA", "cs.MS", "cs.MA", "cs.PF", "stat.AP", "eess.SP", "math.GN",
    #     "nlin.SI", "stat.CO", "eess.AS", "q-bio.OT", "cs.LO", "math.GM", "cs.CE",
    #     "astro-ph.EP", "cs.NE", "q-fin.RM", "astro-ph.CO", "stat.OT", "math.DG",
    #     "math.AG", "math.FA", "math.DS", "math.AC", "cs.PL", "q-bio.QM", "q-bio.MN",
    #     "q-fin.EC", "cs.SY", "cs.HC", "astro-ph.HE", "econ.GN", "cs.OH", "math.RA",
    #     "cs.CC", "cs.DS", "cs.SD", "cs.SE", "q-bio.CB", "q-fin.GN", "cs.DM", "cs.CG",
    #     "cs.FL", "cond-mat.dis-nn", "cond-mat.mes-hall", "cond-mat.mtrl-sci",
    #     "cond-mat.other", "cond-mat.quant-gas", "cond-mat.soft", "cond-mat.stat-mech",
    #     "cond-mat.str-el", "cond-mat.supr-con", "gr-qc", "hep-ex", "hep-lat", "hep-ph",
    #     "hep-th", "math-ph", "nucl-ex", "nucl-th", "physics.acc-ph", "physics.ao-ph",
    #     "physics.app-ph", "physics.atm-clus", "physics.bio-ph", "physics.atom-ph",
    #     "physics.chem-ph", "physics.class-ph", "physics.comp-ph", "physics.data-an",
    #     "physics.ed-ph", "physics.flu-dyn", "physics.gen-ph", "physics.geo-ph",
    #     "physics.hist-ph", "physics.ins-det", "physics.med-ph", "physics.optics",
    #     "physics.plasm-ph", "physics.pop-ph", "physics.soc-ph", "physics.space-ph",
    #     "quant-ph"
    # ]



    # commas = txt.count(".")
    # print(commas)


if __name__ == "__main__":
    main()