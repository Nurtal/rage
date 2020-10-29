


def run_request(request, max_article):
        """
        SCAVANGED FROM BIBOT
        Use the user_request attribute to retrieve a list of PMID
        -> connect to NCBI and submid user_request
        -> extract PMID from user_request, max pmid extracted
           correspond to the max_article attribute
        -> return a list of PMID
        """

        # importation
        from Bio import Entrez
        from Bio.Entrez import efetch, read, esearch
        import json

        ## parameters
        Entrez.email = 'murlock.raspberypi@gmail.com'

        ## connect to NCBI, sned the user request and extract PMID
        pmid_found = []
        handle = esearch(db='pubmed', term=request, retmode='xml', retmax=max_article)
        xml_data = read(handle)
        for pmid in xml_data['IdList']:
            if(pmid not in pmid_found):
                pmid_found.append(pmid)

        ## return list
        return pmid_found



def get_meta_information(pmid):
        """

        SCAVANGED FROM BIBOT


        TODO : update doc
        -> Parse meta data of the article to get the
            - title
            - journal
            - date
            - author list
            - article type
            - institution
            - Abstract
            - Country journal
            - Language
            - Keywords

        -> return a dictionnary with meta information

        Scavange from web BIBOT
        """

        ## importation
        from Bio import Entrez
        from Bio.Entrez import efetch, read


        ## parameters
        Entrez.email = 'murlock.raspberypi@gmail.com'
        title = "NA"
        journal = "NA"
        date = "NA"
        author_list = "NA"
        article_type = "NA"
        institue = "NA"
        language = "NA"
        abstract = "NA"
        keywords = "NA"
        journal_country = "NA"
        meta_information = {}

        ##-------------##
        ## Access data #########################################################
        ##-------------##

        ## Parse XML response #------------------------------------------------#
        try:
            handle = efetch(db='pubmed', id=pmid, retmode='xml', )
            xml_data = read(handle)
            article_data = xml_data['PubmedArticle'][0]['MedlineCitation']["Article"]
            publication_data = xml_data[u'PubmedArticle'][0][u'MedlineCitation']
        except:
            print("[!] Failed to reach article "+str(pmid))
            xml_data = None
            article_data = None
            publication_data = None


        ## Get the article type #----------------------------------------------#
        try:
            article_type = article_data['PublicationTypeList'][0]
        except:
            pass

        ## get the article title #---------------------------------------------#
        try:
            title = article_data['ArticleTitle']
        except:
            pass

        ## get the publication language #--------------------------------------#
        try:
            language = article_data['Language']
        except:
            pass

        ## get the journal country #-------------------------------------------#
        try:
            journal_country = publication_data[u'MedlineJournalInfo'][u'Country']
        except:
            pass

        ## get the list of keywords #------------------------------------------#
        try:
            keywords = publication_data[u'KeywordList']
            if(len(keywords) == 0):
                keywords = "NA"
        except:
            keywords = "NA"
            pass

        ## get the abstract #--------------------------------------------------#
        try:
            abstract = ""
            abstract_data = article_data['Abstract']['AbstractText']
            for element in abstract_data:
                abstract += str(element)+" "
            abstract = abstract[:-1]
        except:
            pass

        ## get the date #------------------------------------------------------#
        try:
            if(len(article_data['ArticleDate'])> 0):
                date_data = article_data['ArticleDate'][0]
                date = str(date_data['Day'])+"/"+str(date_data['Month'])
                date += "/"+str(date_data['Year'])
            else:
                try:
                    date_data = article_data['Journal']['JournalIssue']['PubDate']
                    date = str(date_data['Year'])
                except:
                    date = date_data['MedlineDate']
                    date = date[:4]
        except:
            pass
        ## get the institute #-------------------------------------------------#
        try:
            institue =  article_data['AuthorList'][0]['AffiliationInfo']
            institue = institue[0]['Affiliation']
        except:
            institue = "NA"
            pass

        ## get the list of author #--------------------------------------------#
        try:
            author_data = article_data['AuthorList']
            author_list = ""
            for author in author_data:
                try:
                    author_list += author['LastName']+" "+author['Initials']+", "
                except:
                    pass
            author_list = author_list[:-2]
        except:
            pass

        ## get the journal name #----------------------------------------------#
        try:
            journal = article_data['Journal']['Title']
        except:
            pass


        ##-----------------------##
        ## structure information ###############################################
        ##-----------------------##
        meta_information['title'] = title
        meta_information['journal'] = journal
        meta_information['date'] = date
        meta_information['author_list'] = author_list
        meta_information['article_type'] = article_type
        meta_information['institution'] = institue
        meta_information['language'] = language
        meta_information['abstract'] = abstract
        meta_information['keywords'] = keywords
        meta_information['journal_country'] = journal_country


        ## return information
        return meta_information
