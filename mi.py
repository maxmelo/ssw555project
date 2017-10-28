from ged import compare_dates, date_difference

#sprint 1: stories 5 and 10
#sprint 2: stories 6 and 9
#sprint 3: stories 12 and 21

#Validation check for Marriage date before death date
#Individual cannot have died before they got married
def us05(ged):
    out = []

    #search for individuals stored in 'families'
    for ID in ged['families']:
        family = ged['families'][ID]
        
        #Ensure that each tag is present 'families'
        if not 'HUSB' in family or not 'WIFE' in family or not 'MARR' in family:
            continue

        #Search for HUSB or WIFE tag in family lib
        for person in ['HUSB','WIFE']:

            #check if family member is apart of lib for individuals
            if family[person] in ged['individuals']:
                individual = ged['individuals'][family[person]]
                if 'DEAT' in individual:

                    #compare date stored for 'MARR' with date for 'DEAT'
                    compare = compare_dates(family['MARR'], individual['DEAT'])

                    if compare == 1:
                        out.append('Error US05: Death date of {} ({}) occurs before marriage date'
                                   .format(individual['NAME'],family[person]))
    return out

#Validation Check to ensure divorce date happens before death
def us06(ged):
    out = []

    #search for individuals stored in 'families'
    for ID in ged['families']:
        family = ged['families'][ID]
        
        #Ensure that each tag is present 'families'
        if not 'HUSB' in family or not 'WIFE' in family or not 'DIV' in family:
            continue

        #Search for HUSB or WIFE tag in family lib
        for person in ['HUSB','WIFE']:

            #check if family member is apart of lib for individuals
            if family[person] in ged['individuals']:
                individual = ged['individuals'][family[person]]
                if 'DEAT' in individual:

                    #compare date stored for 'DIV' with date for 'DEAT'
                    compare = compare_dates(family['DIV'], individual['DEAT'])

                    if compare == 1:
                        out.append('Error US06: Divorce date of {} ({}) occurs after Death date'
                                   .format(individual['NAME'],family[person]))
    return out
#Validation check to ensure birth date takes place before death date
def us09(ged):
    out = []

    #search for person stored in 'individuals'
    for ID in ged['individuals']:
        Ind = ged['individuals'][ID]

        #ensure death tag is present
        if not 'DEAT' in Ind:
            continue

        #find person with death tag
        for person in ['DEAT']:
            
            #compare date stored for 'BIRT' with date for 'DEAT'
            compare = compare_dates(Ind['BIRT'], Ind['DEAT'])
            if compare == 1:
                out.append('Error US09: Death date of {} ({}) occurs before birth date'
                            .format(Ind['NAME'],Ind[person]))
    return out

#Validation check to ensure that no marriages occur with a partner under 14 occur
def us10(ged):

    output = []
    for ID in ged['families']:
        family = ged['families'][ID]

        if not family['HUSB'] in ged['individuals'] or not family['WIFE'] in ged['individuals']:
            continue

        husband = ged['individuals'][family['HUSB']]['NAME'] 
        wife = ged['individuals'][family['WIFE']]['NAME'] 
            
        #check for a marriage
        if husband is not None and wife is not None and 'MARR' in family:

            for person in ['HUSB','WIFE']:
                if family[person] in ged['individuals']:
                    individual = ged['individuals'][family[person]]

                    if 'BIRT' in individual:
                    #finds number of days between marriage date and birth date of individual
                        date_diff = date_difference(individual['BIRT'], family['MARR'])

                    #14 years = 5110 days
                        if date_diff < 5110:
                            output.append('Error US10: Marriage of {} and {} ({}, {}) occurs with a parter under age 14'
                                          .format(husband, wife, family['HUSB'], family['WIFE']))

    return output


def us12(ged):
    
    out = []
    #gives us the current date in form "%d %b %Y"
    curr_date = datetime.datetime.today().strftime("%d %b %Y")

    for ID in ged['families']:
        fam = ged['families'][ID]

        #check if family has a husband, wife, and child
        if not 'HUSB' in fam or not 'WIFE' in fam or not 'CHIL' in fam:
            continue
        #find husband in family
        for person in ['HUSB']:
            if fam[person] in ged['individuals']:
                ind = ged['individuals'][fam[person]]
                #only need to compare to first, or oldest, child
                found = ged['individuals'][fam['CHIL'][0]]
                gap = date_difference(ind['BIRT'],found['BIRT'])
                #80 years = 29200
                if gap >= 29200:
                    out.append('Error US12: Father {} ({}) is at least 80 years older than his child'
                               .format(ind['NAME'],fam['HUSB']))

        #find wife in family
        for person in ['WIFE']:
             if fam[person] in ged['individuals']:
                 ind = ged['individuals'][fam[person]]
                 #only need to compare to the first, or oldest, child
                 found = ged['individuals'][fam['CHIL'][0]]
                 gap = date_difference(ind['BIRT'], found['BIRT'])
                 #60 years = 21900 days
                 if gap >= 21900:
                     out.append('Error US12: Mother {} ({}) is at least 60 years older than her child'
                                .format(ind['NAME'],fam['WIFE']))
    return out

def us21(ged):
    out = []
    for ID in ged['families']:
        fam = ged['families'][ID]

        if not 'HUSB' in fam or not 'WIFE' in fam or not 'MARR' in fam:
            continue
                #find husband for each family
        for person in ['HUSB']:
            if fam[person] in ged['individuals']:
                ind = ged['individuals'][fam[person]]
                #check husbands sex tag
                if ind['SEX'] == 'F':
                    out.append('Error US21: Gender of {} ({}) does not match family role'
                                   .format(ind['NAME'],fam['HUSB']))
        for person in ['WIFE']:
            if fam[person] in ged['individuals']:
                ind = ged['individuals'][fam[person]]
                #check wife's sex tag
                if ind['SEX'] == 'M':
                    out.append('Error US21: Gender of {} ({}) does not match family role'
                                   .format(ind['NAME'],fam['WIFE']))
                
    return out

#if __name__ == '__main__':
#    from ged import parse_ged
#    with open('test.ged') as f:
#        parsed = parse_ged(f.read().split('\n'))
#        print(us06(parsed))
