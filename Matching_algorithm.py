# =============================================================================
# Pipeline: Award Paper Matching 
#
#   1. Load paper-level data with discipline, team size, and yearly citations
#   2. Load winner and coauthor publication records
#   3. Merge treatment year and identify treated papers
#   4. Form exact-match groups by type, publication year, discipline, and team size
#   5. Construct pre-treatment citation trajectories
#   6. Match each treated paper to the 20 closest control papers within group
#   7. Save the 1-to-20 matched candidate sample
#   8. Apply distance thresholds and retain the best 1-to-1 match
#   9. Report matching statistics and compare citation trajectories
#  10. Save the final 1-to-1 matched sample
# =============================================================================


import pandas as pd
import numpy as np
import numba as nb
from collections import Counter
from multiprocessing import Pool


def load_winner_coauthor_pubs():
    df = pd.read_csv("./winner_pub_300.csv", usecols=[0,3,4])
    df = df.rename(columns={"publication_year":"pub_year","first_awardYear":"treated_year"})
    df.loc[:,"source"] = "winner_pub_300"

    df2 = pd.read_csv("./coauthor_pub_300.csv", usecols=[0,4,6])
    df2 = df2.rename(columns={"indep_work_id":"work_id","publication_year":"pub_year","first_awardYear":"treated_year"})
    df2.loc[:,"source"] = "coauthor_pub_300"

    out = pd.concat([df, df2], ignore_index=True)
    out.loc[:,"pub_year"] = out.loc[:,"pub_year"].astype(int)
    out.loc[:,"treated_year"] = out.loc[:,"treated_year"].astype(int)
    return out.loc[:,["source","work_id","pub_year","treated_year"]]


def cal_yearlymat(yearlycounter, year):
    if type(yearlycounter) != Counter:
        return np.array([0]*10)
    else:
        return np.array([yearlycounter[_y] for _y in range(year-5, year+5)])

@nb.njit
def cal_dis(_v, _mat):
    if sum(_v)<=10:
        x = _mat-_v
        sum_value = np.sum(x,axis=1)
        sig = np.where(sum_value>=0, 1, -1)
        return 0.1*sig*np.sum(np.abs(x),axis=1)
    else:
        x = _mat-_v
        sum_value = np.sum(x,axis=1)
        sig = np.where(sum_value>=0, 1, -1)
        return sig*np.sum(np.abs(x),axis=1)/(np.sum(_v))

def match_onegroup_yearly20(df):
    res = [pd.DataFrame(
            columns=["work_id","type","publication_year","concept","level","teamsize",
                     "yearlycits","treated_year","treated_paper","yearlymat","distance","matched_group","matched_successful"])
          ]

    if_treated = df.treated_paper==True
    treated_df = df[if_treated].copy()
    match_df = df[~if_treated]

    n_treated_df = len(treated_df)
    n_match_df = len(match_df)

    #print(n_match_df, n_treated_df)
    if (n_treated_df == 0):
        pass
        #return pd.concat(res, ignore_index=True)

    elif (n_match_df == 0):
        _df = treated_df.copy()
        _df["yearlymat"] = _df.apply(lambda x:cal_yearlymat(x["yearlycits"], int(x["treated_year"])), axis=1)
        _df["distance"] = np.nan
        _df["matched_group"] = np.nan
        _df["matched_successful"] = False
        res.append(_df)
        #return pd.concat(res, ignore_index=True)

    else:
        #match top 20
        treated_df["yearlymat"] = treated_df.apply(lambda x:cal_yearlymat(x["yearlycits"], int(x["treated_year"]) ), axis=1)

        for idx, row in treated_df.iterrows():
            #print(row)
            treated_year = int(row["treated_year"])
            _df = match_df.copy()
            _df["yearlymat"] = _df.apply(lambda x:cal_yearlymat(x["yearlycits"], treated_year), axis=1)
            # cal distance
            p_array = row["yearlymat"]
            match_mat = np.stack(_df.yearlymat.values)
            _df["distance"] = cal_dis(p_array[:5], match_mat[:,:5])
            _df = _df.reindex(_df.distance.abs().sort_values().index)

            _df = pd.concat([_df.head(20),row.to_frame().T])
            _df["matched_group"] = row["work_id"]+"_"+ str(int(treated_year))
            _df["matched_successful"] = True
            res.append(_df)

    return pd.concat(res, ignore_index=True)


def cal_mean_sem(v):
    _v = np.stack(v)
    #print(_v.shape)
    m = np.mean(_v, axis=0)
    ci = 1.96*np.std(_v, axis=0)/ np.sqrt(_v.shape[0])

    return ", ".join(["%.3f±%.4f" % (a,b) for a,b in zip(m, ci)])

def get_optimal_match(df, lcut=-0.3, rcut=0.25, n=5):
    g = df.copy()
    g["abs_distance"] = g.distance.apply(lambda x: np.abs(x) if x==x else np.nan)

    g1 = g[g.treated_paper==True]
    g2 = g[g.treated_paper==False]
    g2 = g2[(g2.distance >=lcut)& (g2.distance<=rcut)]
    g2 = g2.sort_values(by='abs_distance', ascending = True)
    g2 = g2.groupby('matched_group').head(n)

    out = pd.concat([g1,g2],axis=0)
    out["groupsize"] = out.groupby("matched_group")["concept"].transform("size") - 1
    out = out.sort_values(by=["matched_group","treated_paper"])

    error = out[out.groupsize>n]
    print("errors:", len(error), "#groups:", len(set(error.matched_group)))
    return out[out.groupsize<=n]




if __name__ == '__main__':
    # pubs_concept_team_cits.pkl includes columns: work_id, type, publication_year, concept, level, teamsize, yearlycits
    pubs_concept_team_cits = pd.read_pickle("../policy_papers_match/pubs_concept_team_cits.pkl")
    pubs_concept_team_cits = pubs_concept_team_cits.dropna(subset=["concept","teamsize"])
    pubs_concept_team_cits["level"] = pubs_concept_team_cits["level"].astype("int")
    pubs_concept_team_cits["teamsize"] = pubs_concept_team_cits["teamsize"].astype("int")
    cols = ['id', 'type', 'publication_year', 'concept','level', 'teamsize', 'yearlycits']
    pubs_concept_team_cits = pubs_concept_team_cits[cols].rename(columns={"id":"work_id"})

    # load winner
    WC_paper = load_winner_coauthor_pubs()
    WC_paper = WC_paper.drop_duplicates()

    # merge pubs and winner data
    pubs_concept_team_cits = pubs_concept_team_cits.merge(WC_paper[["work_id","treated_year"]], on="work_id", how="left")
    pubs_concept_team_cits["treated_paper"] = pubs_concept_team_cits["treated_year"].notnull()
    print(pubs_concept_team_cits.shape)

    # match 1v20
    pool = Pool(processes=40)

    GROUPS = pubs_concept_team_cits.groupby(["type","publication_year","concept","teamsize"], as_index=False)
    print ("total groups:", len(GROUPS))

    res_list = pool.map(match_onegroup_yearly20, [gdf for name, gdf in GROUPS])

    matched_table_yearly = pd.concat(res_list, ignore_index=True)

    matched_table_yearly.to_pickle("./ripple_matched_table_yearly5_1v20.pkl")

    # 1v1 threshold filtering (lcut=-0.1, rcut=0.125, n=1)
    out = get_optimal_match(matched_table_yearly, lcut=-0.1, rcut=0.125, n=1)
    # statistics
    print("unmatched paper:", len(out[out.groupsize==0]))
    print("matched paper:", len( set( out[out.groupsize>=1].matched_group) ))
    print("Average matched papers:", out[out.groupsize>=1].groupby("matched_group")["groupsize"].first().mean() )

    # cit comparison
    print("cit comparison")
    winner_cit  = out[(out.treated_paper==True)&(out.groupsize>=1)].yearlymat.values
    print("treated paper±95%CI: ", cal_mean_sem(winner_cit))

    contender_cit  = out[(out.treated_paper==False)& (out.groupsize>=1)]
    contender_cit = contender_cit.groupby("matched_group", as_index=False).agg(
        {"yearlymat":lambda x:np.mean(np.array(list(x.values)), axis=0)} )
    print ("matched paper±95%CI:", cal_mean_sem(contender_cit.yearlymat.values) )

    save_cols = ['work_id', 'type', 'publication_year', 'concept', 'teamsize',
                 'treated_year', 'treated_paper', 'yearlymat', 'distance', 'matched_group']
    out.loc[out.groupsize==1, save_cols].to_pickle("./ripple_matched_table_yearly5_1v1.pkl")

    #end