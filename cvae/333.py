columns = ["year_data_c", "unique_carrier_c", "origin_c", "origin_state_abr_c", "dest_c", "dest_state_abr_c",
           "dep_delay_n", "taxi_out_n", "taxi_in_n", "arr_delay_n", "air_time_n", "distance_n"]


year_data_c =  {2001: 0, 2011: 1, 2013: 2, 2012: 3, 2009: 4, 2005: 5, 2006: 6, 2007: 7, 2004: 8, 1999: 9, 2000: 10, 2014: 11, 1996: 12, 1997: 13, 2008: 14, 1998: 15, 2003: 16, 1995: 17, 2002: 18, 2015: 19, 2010: 20, 2016: 21}
unique_carrier_c =  {'AA': 0, 'B6': 1, 'US': 2, 'DL': 3, '9E': 4, 'CO': 5, 'OO': 6, 'XE': 7, 'NW': 8, 'UA': 9, 'WN': 10, 'EV': 11, 'AS': 12, 'HP': 13, 'MQ': 14, 'FL': 15, 'YV': 16, 'TW': 17, 'OH (1)': 18, 'F9': 19, 'DH': 20, 'NK': 21, 'HA': 22, 'VX': 23, 'AQ': 24, 'TZ': 25}
origin_c =  {'DFW': 0, 'JFK': 1, 'PIT': 2, 'TPA': 3, 'CLE': 4, 'MSP': 5, 'MSY': 6, 'OMA': 7, 'ATL': 8, 'STL': 9, 'ORF': 10, 'CVG': 11, 'SNA': 12, 'IAH': 13, 'HOU': 14, 'LGA': 15, 'LAX': 16, 'MEM': 17, 'SJC': 18, 'BOS': 19, 'ANC': 20, 'CHS': 21, 'DTW': 22, 'MCI': 23, 'BWI': 24, 'LGB': 25, 'RNO': 26, 'CLT': 27, 'PHX': 28, 'LAS': 29, 'ORD': 30, 'OKC': 31, 'DEN': 32, 'PHL': 33, 'FLL': 34, 'PVD': 35, 'RDU': 36, 'OME': 37, 'MCO': 38, 'SFO': 39, 'DCA': 40, 'BHM': 41, 'XNA': 42, 'VPS': 43, 'SEA': 44, 'SAN': 45, 'DAL': 46, 'BGR': 47, 'SMF': 48, 'MIA': 49, 'IAD': 50, 'ONT': 51, 'GSO': 52, 'EWR': 53, 'SMX': 54, 'BUF': 55, 'SLC': 56, 'HPN': 57, 'MKE': 58, 'GTF': 59, 'CID': 60, 'ITH': 61, 'LSE': 62, 'COD': 63, 'AVP': 64, 'GPT': 65, 'RIC': 66, 'SAT': 67, 'AUS': 68, 'CMH': 69, 'SRQ': 70, 'SJU': 71, 'SIT': 72, 'GRR': 73, 'PDX': 74, 'ECP': 75, 'MDW': 76, 'ROC': 77, 'CAK': 78, 'AMA': 79, 'ISP': 80, 'GEG': 81, 'OAK': 82, 'CDV': 83, 'RSW': 84, 'ABI': 85, 'PNS': 86, 'HRL': 87, 'MHT': 88, 'AZO': 89, 'BTM': 90, 'SBN': 91, 'BNA': 92, 'FAR': 93, 'ABE': 94, 'HNL': 95, 'PBI': 96, 'PFN': 97, 'TRI': 98, 'ILM': 99, 'PSP': 100, 'FCA': 101, 'AVL': 102, 'FNT': 103, 'MOB': 104, 'RST': 105, 'ABQ': 106, 'DSM': 107, 'MLI': 108, 'JAX': 109, 'LEX': 110, 'BDL': 111, 'OTH': 112, 'ELP': 113, 'SDF': 114, 'JAN': 115, 'SYR': 116, 'MDT': 117, 'CAE': 118, 'SBA': 119, 'SAV': 120, 'JAC': 121, 'DHN': 122, 'CPR': 123, 'TUL': 124, 'CIC': 125, 'LIH': 126, 'BUR': 127, 'ALB': 128, 'MOT': 129, 'MYR': 130, 'TUS': 131, 'RAP': 132, 'BTR': 133, 'LBB': 134, 'MSO': 135, 'CHA': 136, 'BZN': 137, 'GRK': 138, 'DBQ': 139, 'TYS': 140, 'ICT': 141, 'APF': 142, 'IND': 143, 'DLH': 144, 'LIT': 145, 'PHF': 146, 'FWA': 147, 'PWM': 148, 'BOI': 149, 'FSD': 150, 'DAY': 151, 'YUM': 152, 'HLN': 153, 'MFE': 154, 'ITO': 155, 'OGG': 156, 'KTN': 157, 'MSN': 158, 'COS': 159, 'TVC': 160, 'BKG': 161, 'PIA': 162, 'GUM': 163, 'FAT': 164, 'HSV': 165, 'GCC': 166, 'ACT': 167, 'DUT': 168, 'SBP': 169, 'VLD': 170, 'EUG': 171, 'ATW': 172, 'MRY': 173, 'TLH': 174, 'SHV': 175, 'CRP': 176, 'JNU': 177, 'CMX': 178, 'MAF': 179, 'EWN': 180, 'LNK': 181, 'SUX': 182, 'MEI': 183, 'GRI': 184, 'SGF': 185, 'GSP': 186, 'STT': 187, 'EVV': 188, 'MLU': 189, 'LFT': 190, 'RDM': 191, 'LRD': 192, 'LAN': 193, 'DRO': 194, 'EGE': 195, 'DAB': 196, 'SCC': 197, 'SPS': 198, 'MOD': 199, 'ASE': 200, 'KOA': 201, 'PSG': 202, 'CLD': 203, 'MGM': 204, 'FLG': 205, 'BTV': 206, 'BIS': 207, 'BGM': 208, 'GRB': 209, 'CWA': 210, 'IDA': 211, 'MFR': 212, 'BQN': 213, 'BFL': 214, 'TYR': 215, 'CMI': 216, 'ACK': 217, 'PIH': 218, 'GUC': 219, 'MBS': 220, 'FAY': 221, 'AKN': 222, 'SPI': 223, 'TXK': 224, 'STX': 225, 'BMI': 226, 'OTZ': 227, 'EYW': 228, 'SJT': 229, 'MLB': 230, 'LCH': 231, 'FAI': 232, 'MHK': 233, 'BRO': 234, 'MTJ': 235, 'WYS': 236, 'ROA': 237, 'GNV': 238, 'MQT': 239, 'ACV': 240, 'BPT': 241, 'EKO': 242, 'ABR': 243, 'OXR': 244, 'TOL': 245, 'CDC': 246, 'HDN': 247, 'AGS': 248, 'SWF': 249, 'GFK': 250, 'CRW': 251, 'BQK': 252, 'LAW': 253, 'PSC': 254, 'CHO': 255, 'FSM': 256, 'PSE': 257, 'ADQ': 258, 'HTS': 259, 'GJT': 260, 'SUN': 261, 'INL': 262, 'ALO': 263, 'RDD': 264, 'SAF': 265, 'ESC': 266, 'WRG': 267, 'ERI': 268, 'BET': 269, 'ACY': 270, 'GGG': 271, 'LYH': 272, 'BRD': 273, 'RKS': 274, 'ART': 275, 'AEX': 276, 'BIL': 277, 'VEL': 278, 'BRW': 279, 'TTN': 280, 'EAU': 281, 'IPL': 282, 'ABY': 283, 'YAK': 284, 'EFD': 285, 'HOB': 286, 'ELM': 287, 'SGU': 288, 'GTR': 289, 'TUP': 290, 'PLN': 291, 'DIK': 292, 'CLL': 293, 'TWF': 294, 'OAJ': 295, 'TEX': 296, 'VIS': 297, 'IYK': 298, 'CEC': 299, 'FLO': 300, 'PAH': 301, 'ISN': 302, 'LBE': 303, 'CSG': 304, 'ROW': 305, 'ORH': 306, 'SCE': 307, 'ILE': 308, 'CIU': 309, 'JLN': 310, 'PUB': 311, 'COU': 312, 'MCN': 313, 'DRT': 314, 'JMS': 315, 'LWB': 316, 'KSM': 317, 'BJI': 318, 'PIE': 319, 'MKG': 320, 'BLI': 321, 'PMD': 322, 'LWS': 323, 'LAR': 324, 'RFD': 325, 'GCK': 326, 'RHI': 327, 'PPG': 328, 'IMT': 329, 'LMT': 330, 'DLG': 331, 'LNY': 332, 'FOE': 333, 'ILG': 334, 'ISO': 335, 'GST': 336, 'APN': 337, 'IAG': 338, 'MMH': 339, 'HIB': 340, 'SPN': 341, 'HKY': 342, 'HHH': 343, 'MAZ': 344, 'PIB': 345, 'HVN': 346, 'HYS': 347, 'DVL': 348, 'VCT': 349, 'PBG': 350, 'ADK': 351, 'MVY': 352, 'CNY': 353, 'UTM': 354, 'YKM': 355, 'SLE': 356, 'MIB': 357, 'MWH': 358, 'STC': 359, 'HYA': 360, 'UST': 361, 'CYS': 362, 'CKB': 363, 'SOP': 364, 'MTH': 365, 'ANI': 366, 'RDR': 367, 'MKK': 368, 'SHD': 369, 'AZA': 370, 'PGD': 371}
origin_state_abr_c =  {'TX': 0, 'NY': 1, 'PA': 2, 'FL': 3, 'OH': 4, 'MN': 5, 'LA': 6, 'NE': 7, 'GA': 8, 'MO': 9, 'VA': 10, 'KY': 11, 'CA': 12, 'TN': 13, 'MA': 14, 'AK': 15, 'SC': 16, 'MI': 17, 'MD': 18, 'NV': 19, 'NC': 20, 'AZ': 21, 'IL': 22, 'OK': 23, 'CO': 24, 'RI': 25, 'AL': 26, 'AR': 27, 'WA': 28, 'ME': 29, 'NJ': 30, 'UT': 31, 'WI': 32, 'MT': 33, 'IA': 34, 'WY': 35, 'MS': 36, 'PR': 37, 'OR': 38, 'NH': 39, 'IN': 40, 'ND': 41, 'HI': 42, 'NM': 43, 'CT': 44, 'SD': 45, 'KS': 46, 'ID': 47, 'TT': 48, 'VI': 49, 'VT': 50, 'WV': 51, 'DE': 52}
dest_c =  {'MCI': 0, 'BTV': 1, 'PHX': 2, 'ATL': 3, 'CLT': 4, 'EWR': 5, 'SLC': 6, 'RDU': 7, 'DFW': 8, 'IAH': 9, 'MSP': 10, 'SFO': 11, 'AUS': 12, 'LAS': 13, 'BNA': 14, 'JNU': 15, 'PIT': 16, 'MCN': 17, 'PVD': 18, 'MCO': 19, 'JFK': 20, 'ORD': 21, 'BOI': 22, 'IAD': 23, 'ONT': 24, 'SAN': 25, 'SYR': 26, 'SJU': 27, 'SEA': 28, 'MDW': 29, 'TPA': 30, 'DTW': 31, 'ANC': 32, 'ELP': 33, 'LAX': 34, 'DEN': 35, 'BWI': 36, 'MSY': 37, 'SWF': 38, 'COS': 39, 'PHL': 40, 'CLE': 41, 'SNA': 42, 'BUF': 43, 'HOU': 44, 'PWM': 45, 'RNO': 46, 'LEX': 47, 'SMF': 48, 'DCA': 49, 'DAY': 50, 'PBI': 51, 'BOS': 52, 'LIT': 53, 'SAV': 54, 'RSW': 55, 'BMI': 56, 'LGB': 57, 'MIA': 58, 'GTF': 59, 'IND': 60, 'SJC': 61, 'PDX': 62, 'MKE': 63, 'TYS': 64, 'OAK': 65, 'SAT': 66, 'STL': 67, 'SGF': 68, 'LNK': 69, 'MYR': 70, 'FAT': 71, 'CAK': 72, 'CVG': 73, 'PSP': 74, 'GSO': 75, 'ERI': 76, 'ROC': 77, 'EUG': 78, 'ROA': 79, 'HSV': 80, 'DAL': 81, 'MEM': 82, 'CMH': 83, 'TRI': 84, 'TUL': 85, 'YAK': 86, 'CLL': 87, 'MSN': 88, 'VPS': 89, 'KOA': 90, 'SDF': 91, 'JAN': 92, 'FLL': 93, 'BUR': 94, 'MGM': 95, 'ALB': 96, 'CRP': 97, 'GEG': 98, 'MBS': 99, 'MSO': 100, 'BDL': 101, 'LBB': 102, 'MHT': 103, 'RDM': 104, 'TUS': 105, 'RIC': 106, 'ABQ': 107, 'GRB': 108, 'OMA': 109, 'FSD': 110, 'FAI': 111, 'MAF': 112, 'OKC': 113, 'LIH': 114, 'KTN': 115, 'HPN': 116, 'BHM': 117, 'LGA': 118, 'ACV': 119, 'MDT': 120, 'JAX': 121, 'SMX': 122, 'GPT': 123, 'CLD': 124, 'ABE': 125, 'HNL': 126, 'OTZ': 127, 'BIL': 128, 'AVL': 129, 'YUM': 130, 'OGG': 131, 'GRR': 132, 'STT': 133, 'PIA': 134, 'GNV': 135, 'XNA': 136, 'SBN': 137, 'PNS': 138, 'GCC': 139, 'SHV': 140, 'MTJ': 141, 'DSM': 142, 'BTR': 143, 'MRY': 144, 'PHF': 145, 'SBP': 146, 'GSP': 147, 'ABI': 148, 'SBA': 149, 'LAN': 150, 'ISP': 151, 'FAR': 152, 'CAE': 153, 'AMA': 154, 'FWA': 155, 'BPT': 156, 'CHS': 157, 'BGR': 158, 'ORF': 159, 'CMI': 160, 'TWF': 161, 'CID': 162, 'RST': 163, 'EVV': 164, 'FNT': 165, 'SIT': 166, 'IDA': 167, 'GFK': 168, 'DHN': 169, 'ICT': 170, 'ISN': 171, 'MHK': 172, 'PSG': 173, 'ILM': 174, 'BZN': 175, 'TYR': 176, 'TLH': 177, 'FCA': 178, 'ITO': 179, 'DRO': 180, 'LFT': 181, 'LSE': 182, 'DAB': 183, 'AZO': 184, 'CSG': 185, 'BRO': 186, 'STX': 187, 'BLI': 188, 'SRQ': 189, 'CPR': 190, 'HRL': 191, 'COD': 192, 'RAP': 193, 'PSC': 194, 'GRK': 195, 'LRD': 196, 'FSM': 197, 'LCH': 198, 'BRW': 199, 'FAY': 200, 'BET': 201, 'WRG': 202, 'VLD': 203, 'MOB': 204, 'ABY': 205, 'ROW': 206, 'LWS': 207, 'GTR': 208, 'MFE': 209, 'LAW': 210, 'ADQ': 211, 'GJT': 212, 'SGU': 213, 'ATW': 214, 'BGM': 215, 'JAC': 216, 'ASE': 217, 'HIB': 218, 'OXR': 219, 'CRW': 220, 'BQK': 221, 'ILE': 222, 'BFL': 223, 'OME': 224, 'LMT': 225, 'MLU': 226, 'CHA': 227, 'MLI': 228, 'ABR': 229, 'AVP': 230, 'MOT': 231, 'BTM': 232, 'DLH': 233, 'ALO': 234, 'PFN': 235, 'SJT': 236, 'RDD': 237, 'HYS': 238, 'BRD': 239, 'AEX': 240, 'MLB': 241, 'OTH': 242, 'EYW': 243, 'BQN': 244, 'PBG': 245, 'CHO': 246, 'CMX': 247, 'OAJ': 248, 'BIS': 249, 'RKS': 250, 'HYA': 251, 'TVC': 252, 'AGS': 253, 'IPL': 254, 'BKG': 255, 'ORH': 256, 'COU': 257, 'PSE': 258, 'GGG': 259, 'GUC': 260, 'HDN': 261, 'SPI': 262, 'SUX': 263, 'INL': 264, 'CDV': 265, 'EFD': 266, 'HLN': 267, 'TOL': 268, 'MFR': 269, 'ACT': 270, 'MVY': 271, 'TXK': 272, 'SPS': 273, 'EKO': 274, 'SHD': 275, 'FLG': 276, 'GRI': 277, 'EGE': 278, 'HKY': 279, 'SUN': 280, 'ACY': 281, 'MEI': 282, 'GUM': 283, 'DBQ': 284, 'TTN': 285, 'ECP': 286, 'MOD': 287, 'FLO': 288, 'PLN': 289, 'ISO': 290, 'MQT': 291, 'LYH': 292, 'LAR': 293, 'SCC': 294, 'DIK': 295, 'PIH': 296, 'LWB': 297, 'ELM': 298, 'GCK': 299, 'WYS': 300, 'EWN': 301, 'SAF': 302, 'CEC': 303, 'JMS': 304, 'DVL': 305, 'DLG': 306, 'ITH': 307, 'CIC': 308, 'AKN': 309, 'ESC': 310, 'PIB': 311, 'CWA': 312, 'DUT': 313, 'RHI': 314, 'PAH': 315, 'IYK': 316, 'RFD': 317, 'CNY': 318, 'LBE': 319, 'SCE': 320, 'CIU': 321, 'BJI': 322, 'CDC': 323, 'CYS': 324, 'VIS': 325, 'MWH': 326, 'JLN': 327, 'HTS': 328, 'PUB': 329, 'YKM': 330, 'GST': 331, 'MKK': 332, 'VCT': 333, 'EAU': 334, 'APF': 335, 'PIE': 336, 'RDR': 337, 'SLE': 338, 'ACK': 339, 'ILG': 340, 'IMT': 341, 'LNY': 342, 'MKG': 343, 'MMH': 344, 'FOE': 345, 'UST': 346, 'VEL': 347, 'ADK': 348, 'HVN': 349, 'HOB': 350, 'PMD': 351, 'SOP': 352, 'TEX': 353, 'STC': 354, 'TUP': 355, 'ART': 356, 'APN': 357, 'DRT': 358, 'HHH': 359, 'ANI': 360, 'MIB': 361, 'IAG': 362, 'KSM': 363, 'MTH': 364, 'PPG': 365, 'UTM': 366, 'PIR': 367, 'AZA': 368, 'MAZ': 369, 'PGD': 370, 'CKB': 371}
dest_state_abr_c =  {'MO': 0, 'VT': 1, 'AZ': 2, 'GA': 3, 'NC': 4, 'NJ': 5, 'UT': 6, 'TX': 7, 'MN': 8, 'CA': 9, 'NV': 10, 'TN': 11, 'AK': 12, 'PA': 13, 'RI': 14, 'FL': 15, 'NY': 16, 'IL': 17, 'ID': 18, 'VA': 19, 'PR': 20, 'WA': 21, 'MI': 22, 'CO': 23, 'MD': 24, 'LA': 25, 'OH': 26, 'ME': 27, 'KY': 28, 'MA': 29, 'AR': 30, 'MT': 31, 'IN': 32, 'OR': 33, 'WI': 34, 'NE': 35, 'SC': 36, 'AL': 37, 'OK': 38, 'HI': 39, 'MS': 40, 'CT': 41, 'NH': 42, 'NM': 43, 'SD': 44, 'VI': 45, 'WY': 46, 'IA': 47, 'ND': 48, 'KS': 49, 'WV': 50, 'TT': 51, 'DE': 52}


cate_dicts = {"year_data_c":year_data_c,"unique_carrier_c":unique_carrier_c,"origin_c":origin_c,
             "origin_state_abr_c":origin_state_abr_c,"dest_c":dest_c,"dest_state_abr_c":dest_state_abr_c}
cate_cols = cate_dicts.keys()


def mask(indexs, pres):
    # repeat = "nan\tnan\tnan\tnan\tnan\tnan\tnan\tnan\tnan\tnan\t0\tnan"
    mask = ["nan","nan","nan","nan","nan","nan","nan","nan","nan","nan","nan","nan"]

    for n, i in enumerate(indexs):
        pre = pres[n]
        cols = columns[i]
        #print(cols)
        if cols in cate_cols:
            if pre[0] == '"' and pre[-1] == '"':
                dict_key = pre.strip("\"")
            else:
                dict_key = int(pre)
            #print(dict_key)
            pre = cate_dicts[cols][dict_key]
            #print(1)
        mask[i] = str(pre)
    mask_str = mask[0]
    for m in mask[1:]:
        mask_str = mask_str + "\t" + m
    mask_str = mask_str.strip("\t")
    return mask_str


if __name__ == '__main__':
    sqls = [
        'SELECT AVG(dep_delay_n) FROM flights WHERE origin_c = "DFW" AND dest_c = "BTV";',
        'SELECT AVG(arr_delay_n) FROM flights WHERE origin_state_abr_c = "OH";',
        'SELECT SUM(distance_n) FROM flights WHERE year_data_c = 2014 AND unique_carrier_c = "DL";'
    ]

    for sql in sqls:
        if ";" in sql:
            sql = sql.strip()
            sql = sql[:-1]
        where = sql.split("WHERE")[1].strip()
        if "(" in where:
            where = where.split("(")[1]
            where = where.split(")")[0].strip()
        if "AND" in where:
            predicates = where.split("AND")
            for n, j in enumerate(predicates):
                predicates[n] = j.strip()
        else:
            predicates = [where]
        # print(predicates)
        indexs = []
        pres = []
        for j in predicates:
            col = j.split("=")[0].strip()
            pre = j.split("=")[1].strip()
            indexs.append(columns.index(col))
            # print(col)
            pres.append(pre)
        # print(indexs)

        mask_str = mask(indexs, pres)
        print(mask_str)
