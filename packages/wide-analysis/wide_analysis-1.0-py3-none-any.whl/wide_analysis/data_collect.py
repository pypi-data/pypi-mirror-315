from datetime import datetime
from wide_analysis.data import process_data, collect_data_wikidata_ent, collect_data_wikidata_prop, collect_data_wikinews, collect_data_wikiquote, collect_data_es, collect_data_gr
from datasets import load_dataset

def normalize_outcome(o):
    lowered = o.lower()
    if 'διαγρ' in lowered:
        return 'Διαγραφή'
    elif 'διατήρη' in lowered or 'παραμονή' in lowered:
        return 'Διατήρηση'
    elif 'συγχών' in lowered:
        return 'συγχώνευση'
    else:
        return 'Δεν υπάρχει συναίνεση'

def collect(mode, start_date=None, end_date=None, url=None, title=None, output_path=None,
            platform=None, lang=None):
    """
    Collects discussion data from various platforms and languages.

    Parameters:
    - mode: one of ['date_range', 'date', 'title', 'url', 'wide_2023']
    - start_date: a robust parameter that can represent different date/year formats depending on platform/lang.
        Examples:
          * For Spanish Wikipedia year mode: 'dd/mm/yyyy'
          * For Greek Wikipedia title mode: 'mm/yyyy'
          * For English Wikidata/Wikinews: 'YYYY-MM-DD' or just a year derivation
    - end_date: optional, used when needing a date range (e.g., year range).
    - url: the discussion URL
    - title: the title of the page
    - platform: 'wikipedia', 'wikidata_entity', 'wikidata_property', 'wikinews', 'wikiquote'
    - lang: 'en', 'es', 'gr'

    Returns:
    A Pandas DataFrame containing the discussion data, or None if not found.
    """
    if mode not in ['date_range', 'date', 'title', 'url', 'wide_2023']:
        raise ValueError("Invalid mode. Choose from ['date_range', 'date', 'title', 'url', 'wide_2023']")

    if mode == 'wide_2023':
        dataset = load_dataset('hsuvaskakoty/wide_analysis')
        print('Dataset loaded successfully as huggingface dataset')
        print('The dataset has the following columns:', dataset.column_names)
        return dataset

    underlying_mode = mode if mode not in ['date', 'date_range'] else 'year'
    
    if platform is None and lang is None or (platform == 'wikipedia' and lang == 'en'):
        if mode in ['date_range', 'date', 'title']:
            return process_data.prepare_dataset(
                mode=mode,
                start_date=start_date,
                end_date=end_date,
                url=url,
                title=title,
                output_path=output_path
            )
        else:
            print("Invalid input. Choose from ['date_range', 'date', 'title', 'wide_2023']")
            return None

    if platform == 'wikidata_entity':
        if underlying_mode == 'title':
            if not title:
                raise ValueError("For 'title' mode in wikidata entity, 'title' must be provided.")
            return collect_data_wikidata_ent.collect_wikidata_entity(mode='title', title=title, years=[])
        elif underlying_mode == 'year':
            if start_date and end_date:
                start_year = int(datetime.strptime(start_date, "%Y-%m-%d").year)
                end_year = int(datetime.strptime(end_date, "%Y-%m-%d").year)
                return collect_data_wikidata_ent.collect_wikidata_entity(mode='year', years=[start_year, end_year])
            elif start_date:
                single_year = int(datetime.strptime(start_date, "%Y-%m-%d").year)
                return collect_data_wikidata_ent.collect_wikidata_entity(mode='year', years=single_year)
            else:
                raise ValueError("For 'year' mode in wikidata entity, start_date is required.")
        elif underlying_mode == 'url':
            if not url:
                raise ValueError("For 'url' mode in wikidata entity, 'url' must be provided.")
            return collect_data_wikidata_ent.collect_wikidata_entity(mode='url', url=url)
        else:
            raise ValueError("Invalid mode for wikidata entity. Use 'title', 'url', or 'year'.")

    elif platform == 'wikidata_property':
        if underlying_mode == 'title':
            if not title:
                raise ValueError("For 'title' mode in wikidata property, 'title' must be provided.")
            return collect_data_wikidata_prop.collect_wikidata(mode='title', title=title, years=[])
        elif underlying_mode == 'url':
            if not url:
                raise ValueError("For 'url' mode in wikidata property, 'url' must be provided.")
            return collect_data_wikidata_prop.collect_wikidata(mode='url', title='', url=url, years=[])
        elif underlying_mode == 'year':
            if start_date and end_date:
                start_year = int(datetime.strptime(start_date, "%Y-%m-%d").year)
                end_year = int(datetime.strptime(end_date, "%Y-%m-%d").year)
                return collect_data_wikidata_prop.collect_wikidata(mode='year', years=[start_year, end_year])
            elif start_date:
                single_year = int(datetime.strptime(start_date, "%Y-%m-%d").year)
                return collect_data_wikidata_prop.collect_wikidata(mode='year', years=single_year)
            else:
                raise ValueError("For 'year' mode in wikidata property, start_date is required.")
        else:
            raise ValueError("Invalid mode for wikidata property. Use 'title', 'url', or 'year'.")

    elif platform == 'wikinews':
        if underlying_mode == 'title':
            if not title:
                raise ValueError("For 'title' mode in wikinews, 'title' is required.")
            return collect_data_wikinews.collect_wikinews(mode='title', title=title)
        elif underlying_mode == 'url':
            if not url:
                raise ValueError("For 'url' mode in wikinews, 'url' is required.")
            return collect_data_wikinews.collect_wikinews(mode='url', url=url)
        elif underlying_mode == 'year':
            if start_date and end_date:
                start_y = int(datetime.strptime(start_date, "%Y-%m-%d").year)
                end_y = int(datetime.strptime(end_date, "%Y-%m-%d").year)
                return collect_data_wikinews.collect_wikinews(mode='year', year=[start_y, end_y])
            elif start_date:
                single_y = int(datetime.strptime(start_date, "%Y-%m-%d").year)
                return collect_data_wikinews.collect_wikinews(mode='year', year=single_y)
            else:
                raise ValueError("For 'year' mode in wikinews, start_date is required.")
        else:
            raise ValueError("Invalid mode for wikinews. Use 'title', 'url', or 'year'.")

    elif platform == 'wikiquote':
        if underlying_mode == 'title':
            if not title:
                title = 'all'
            return collect_data_wikiquote.collect_wikiquote(mode='title', title=title)
        elif underlying_mode == 'url':
            if not url:
                raise ValueError("For 'url' mode in wikiquote, 'url' must be provided.")
            return collect_data_wikiquote.collect_wikiquote(mode='url', url=url)
        else:
            raise ValueError("Wikiquote collection currently only supports 'title' or 'url' mode.")

    elif platform == 'wikipedia':
        if lang == 'es':
            if underlying_mode == 'title':
                if not title or (start_date and start_date.strip()):
                    raise ValueError("For 'title' mode in Spanish Wikipedia, 'title' must be provided and start_date must be empty.")
                return collect_data_es.collect_es(mode='title', title=title, date='')
            
            elif underlying_mode == 'url':
                if not url:
                    raise ValueError("For 'url' mode in Spanish Wikipedia, 'url' must be provided.")
                return collect_data_es.collect_es(mode='url', title='', url=url)
            
            elif underlying_mode == 'year':
                start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%d/%m/%Y")
                if not start_date:
                    raise ValueError("For 'year' mode in Spanish Wikipedia, start_date (dd/mm/yyyy) is required.")
                return collect_data_es.collect_es(mode='year', title='', date=start_date)
            else:
                raise ValueError("Invalid mode for Spanish Wikipedia. Use 'title' or 'year'.")

        elif lang == 'gr':
            if underlying_mode == 'title':
                if not title or not start_date or len(start_date.split('/')) != 2:
                    raise ValueError("For 'title' mode in Greek Wikipedia, 'title' and start_date='mm/yyyy' are required.")
                return collect_data_gr.collect_gr(mode='title', title=title, years=[start_date])
            elif underlying_mode == 'year':
                if start_date and end_date:
                    start_y = int(datetime.strptime(start_date, "%Y-%m-%d").year)
                    end_y = int(datetime.strptime(end_date, "%Y-%m-%d").year)
                    return collect_data_gr.collect_gr(mode='year', title='', years=[start_y, end_y])
                elif start_date:
                    single_y = int(datetime.strptime(start_date, "%Y-%m-%d").year)
                    return collect_data_gr.collect_gr(mode='year', title='', years=[single_y])
                else:
                    raise ValueError("For 'year' mode in Greek Wikipedia, start_date is required.")
            else:
                raise ValueError("Invalid mode for Greek Wikipedia. Use 'title' or 'year'.")

        else:
            raise ValueError("Invalid lang for wikipedia. Use 'en', 'es', or 'gr'.")

    else:
        raise ValueError("Invalid platform. Use 'wikipedia', 'wikidata_entity', 'wikidata_property', 'wikinews', or 'wikiquote'.")



# from datetime import datetime
# from wide_analysis.data.process_data import prepare_dataset
# from datasets import load_dataset

# from wide_analysis.data.collect_data_wikidata_ent import collect_wikidata_entity, process_discussions_by_url_list
# from wide_analysis.data.collect_data_wikidata_prop import collect_wikidata
# from wide_analysis.data.collect_data_wikinews import collect_wikinews
# from wide_analysis.data.collect_data_wikiquote import collect_wikiquote
# from wide_analysis.data.collect_data_es import collect_es
# from wide_analysis.data.collect_data_gr import collect_gr

# def normalize_outcome(o):
#     lowered = o.lower()
#     if 'διαγρ' in lowered:
#         return 'Διαγραφή'
#     elif 'διατήρη' in lowered or 'παραμονή' in lowered:
#         return 'Διατήρηση'
#     elif 'συγχών' in lowered:
#         return 'συγχώνευση'
#     else:
#         return 'Δεν υπάρχει συναίνεση'

# def collect(mode, start_date=None, end_date=None, url=None, title=None, output_path=None,
#             platform=None, lang=None):
#     """
#     Collects discussion data from various platforms and languages.

#     Parameters:
#     - mode: one of ['date_range', 'date', 'title', 'url', 'wide_2023']
#     - start_date: a robust parameter that can represent different date/year formats depending on platform/lang.
#         Examples:
#           * For Spanish Wikipedia year mode: 'dd/mm/yyyy'
#           * For Greek Wikipedia title mode: 'mm/yyyy'
#           * For English Wikidata/Wikinews: 'YYYY-MM-DD' or just a year derivation
#     - end_date: optional, used when needing a date range (e.g., year range).
#     - url: the discussion URL
#     - title: the title of the page
#     - platform: 'wikipedia', 'wikidata_entity', 'wikidata_property', 'wikinews', 'wikiquote'
#     - lang: 'en', 'es', 'gr'

#     Returns:
#     A Pandas DataFrame containing the discussion data, or None if not found.
#     """
#     if mode not in ['date_range', 'date', 'title','url','wide_2023']:
#         raise ValueError("Invalid mode. Choose from ['date_range', 'date', 'title','url','wide_2023']")

#     if mode == 'wide_2023':
#         dataset = load_dataset('hsuvaskakoty/wide_analysis')
#         print('Dataset loaded successfully as huggingface dataset')
#         print('The dataset has the following columns:', dataset.column_names)
#         return dataset

#     underlying_mode = mode
#     if mode in ['date', 'date_range']:
#         underlying_mode = 'year'
#     if mode == 'url':
#         underlying_mode = 'url'
#     if (platform is None and lang is None) or (platform=='wikipedia' and lang=='en'):
#         if mode in ['date_range', 'date', 'title']:
#             return prepare_dataset(
#                 mode=mode,
#                 start_date=start_date,
#                 end_date=end_date,
#                 url=url,
#                 title=title,
#                 output_path=output_path
#             )
#         else:
#             print("Invalid input. Choose from ['date_range', 'date', 'title','wide_2023']")
#             return None

#     if platform == 'wikidata_entity':
#         if underlying_mode == 'title':
#             if not title:
#                 raise ValueError("For 'title' mode in wikidata entity, 'title' must be provided.")
#             return collect_wikidata_entity(mode='title', title=title, years=[])
#         elif underlying_mode == 'year':
#             if start_date and end_date:
#                 start_year = int(datetime.strptime(start_date, "%Y-%m-%d").year)
#                 end_year = int(datetime.strptime(end_date, "%Y-%m-%d").year)
#                 return collect_wikidata_entity(mode='year', years=[start_year, end_year])
#             elif start_date:
#                 single_year = int(datetime.strptime(start_date, "%Y-%m-%d").year)
#                 return collect_wikidata_entity(mode='year', years=single_year)
#             else:
#                 raise ValueError("For 'year' mode in wikidata entity, start_date is required.")
#         elif underlying_mode == 'url':
#             if not url:
#                 raise ValueError("For 'url' mode in wikidata entity, 'url' must be provided.")
#             return collect_wikidata_entity(mode='url', url=url)
#         else:
#             raise ValueError("Invalid mode for wikidata entity. Use 'title', 'url', or 'year'.")

#     elif platform == 'wikidata_property':
#         if underlying_mode == 'title':
#             if not title:
#                 raise ValueError("For 'title' mode in wikidata property, 'title' must be provided.")
#             return collect_wikidata(mode='title', title=title, years=[])
#         elif underlying_mode == 'url':
#             if not url:
#                 raise ValueError("For 'url' mode in wikidata property, 'url' must be provided.")
#             return collect_wikidata(mode='url', title='', url=url, years=[])
#         elif underlying_mode == 'year':
#             # Similar to wikidata_entity
#             if start_date and end_date:
#                 start_year = int(datetime.strptime(start_date, "%Y-%m-%d").year)
#                 end_year = int(datetime.strptime(end_date, "%Y-%m-%d").year)
#                 return collect_wikidata(mode='year', years=[start_year, end_year])
#             elif start_date:
#                 single_year = int(datetime.strptime(start_date, "%Y-%m-%d").year)
#                 return collect_wikidata(mode='year', years=single_year)
#             else:
#                 raise ValueError("For 'year' mode in wikidata property, start_date is required.")
#         else:
#             raise ValueError("Invalid mode for wikidata property. Use 'title', 'url', or 'year'.")

#     elif platform == 'wikinews':
#         if underlying_mode == 'title':
#             if not title:
#                 raise ValueError("For 'title' mode in wikinews, 'title' is required.")
#             return collect_wikinews(mode='title', title=title)
#         elif underlying_mode == 'url':
#             if not url:
#                 raise ValueError("For 'url' mode in wikinews, 'url' is required.")
#             return collect_wikinews(mode='url', url=url)
#         elif underlying_mode == 'year':
#             if start_date and end_date:
#                 start_y = int(datetime.strptime(start_date, "%Y-%m-%d").year)
#                 end_y = int(datetime.strptime(end_date, "%Y-%m-%d").year)
#                 return collect_wikinews(mode='year', year=[start_y, end_y])
#             elif start_date:
#                 single_y = int(datetime.strptime(start_date, "%Y-%m-%d").year)
#                 return collect_wikinews(mode='year', year=single_y)
#             else:
#                 raise ValueError("For 'year' mode in wikinews, start_date is required.")
#         else:
#             raise ValueError("Invalid mode for wikinews. Use 'title', 'url', or 'year'.")

#     elif platform == 'wikiquote':
#         if underlying_mode == 'title':
#             if not title:
#                 title = 'all'
#             return collect_wikiquote(mode='title', title=title)
#         elif underlying_mode == 'url':
#             if not url:
#                 raise ValueError("For 'url' mode in wikiquote, 'url' must be provided.")
#             return collect_wikiquote(mode='url', url=url)
#         else:
#             raise ValueError("Wikiquote collection currently only supports 'title' or 'url' mode.")

#     elif platform == 'wikipedia':
#         if lang == 'es':
#             if underlying_mode == 'title':
#                 if not title or (start_date and start_date.strip()):
#                     raise ValueError("For 'title' mode in Spanish Wikipedia, 'title' must be provided and start_date must be empty.")
#                 return collect_es(mode='title', title=title, date='')
#             elif underlying_mode == 'year':
#                 start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%d/%m/%Y")
#                 print(start_date)
#                 if not start_date:
#                     raise ValueError("For 'year' mode in Spanish Wikipedia, start_date (dd/mm/yyyy) is required.")
#                 return collect_es(mode='year', title='', date=start_date)
#             else:
#                 raise ValueError("Invalid mode for Spanish Wikipedia. Use 'title' or 'year'.")

#         elif lang == 'gr':
#             if underlying_mode == 'title':
#                 if not title or not start_date or len(start_date.split('/')) != 2:
#                     raise ValueError("For 'title' mode in Greek Wikipedia, 'title' and start_date='mm/yyyy' are required.")
#                 return collect_gr(mode='title', title=title, years=[start_date])
#             elif underlying_mode == 'year':
#                 if start_date and end_date:
#                     start_y = int(datetime.strptime(start_date, "%Y-%m-%d").year)
#                     end_y = int(datetime.strptime(end_date, "%Y-%m-%d").year)
#                     return collect_gr(mode='year', title='', years=[start_y,end_y])
#                 elif start_date:
#                     single_y = int(datetime.strptime(start_date, "%Y-%m-%d").year)
#                     return collect_gr(mode='year', title='', years=[single_y])
#                 else:
#                     raise ValueError("For 'year' mode in Greek Wikipedia, start_date is required.")
#             else:
#                 raise ValueError("Invalid mode for Greek Wikipedia. Use 'title' or 'year'.")

#         else:
#             raise ValueError("Invalid lang for wikipedia. Use 'en', 'es', or 'gr'.")

#     else:
#         raise ValueError("Invalid platform. Use 'wikipedia', 'wikidata_entity', 'wikidata_property', 'wikinews', or 'wikiquote'.")
