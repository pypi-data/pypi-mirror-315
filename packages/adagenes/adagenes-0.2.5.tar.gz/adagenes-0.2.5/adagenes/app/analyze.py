import os, datetime
import adagenes as ag
import onkopus as op

sample_file = "/somaticMutations.l520.GRCh38.vcf"

def recognize_column_types(list):
    column_type = None
    consistent_type = None

    for value in list:

        if value is None:
            continue
        elif value == "":
            continue

        try:
            val = int(value)
            column_type = 'integer'
            continue
        except:
            pass

        try:
            val = float(value)
            column_type = 'float'
            continue
        except:
            pass

        column_type = 'string'

        if column_type is not None:
            if column_type != consistent_type:
                if (column_type=="integer") and (consistent_type == "float"):
                    column_type = "float"
                elif ((column_type == "integer") or (column_type == "float")) and (consistent_type == "string"):
                    column_type = "string"

        consistent_type = column_type

    return column_type


def find_newest_file(directory):
    """
    Find the newest file in the given directory.
    """
    try:
        # List all files in the directory
        files = [os.path.join(directory, f) for f in os.listdir(directory) if
                 os.path.isfile(os.path.join(directory, f))]

        if not files:
            print("No files found in the directory.")
            return None

        # Find the newest file based on modification time
        newest_file = max(files, key=os.path.getmtime)

        print(f"Newest file: {newest_file}")
        return newest_file
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def load_file(qid, data_dir, start_row=None, end_row=None):
    """

    :param qid:
    :param data_dir:
    :return:
    """
    data_dir = data_dir + "/" + qid
    #files = [f for f in listdir(data_dir) if isfile(join(data_dir, f))]
    #infile = data_dir + "/" + files[0]
    infile = find_newest_file(data_dir)
    if qid == "sample":
        infile = data_dir + sample_file
    print(infile)

    bframe = ag.read_file(infile, start_row=start_row, end_row=end_row)
    #print(bframe.data)

    return bframe


def get_column_defs(output_format):
    pass


def get_magic_obj(key, genome_version):
    if key == "clinvar":
        return op.ClinVarClient(genome_version=genome_version)
    elif key == 'protein':
        return op.UTAAdapterClient(genome_version=genome_version)
    else:
        return None


def annotate_qid(qid, annotations, genome_version=None, data_dir=None, output_format='vcf'):
    for key in annotations.keys():
        if annotations[key]:
            print("Annotate: ", key, " ", qid)

            data_dir = data_dir + "/" + qid
            infile = find_newest_file(data_dir)
            if qid == "sample":
                infile= data_dir + sample_file

            datetime_str = str(datetime.datetime.now())
            outfile = infile + datetime_str + "_" + ".ann." + output_format

            magic_obj = get_magic_obj(key, genome_version)
            ag.process_file(infile, outfile, magic_obj)

            print("File annotated: ",outfile)


    # Generate new column definitions:
    #, cellClass: "rag-blue"

def analyze_uploaded_file(qid, data_dir = None, start_row=None, end_row=None, genome_version="hg38",
                          output_format="vcf", annotate=None):
    """

    :param qid:
    :param data_dir:
    :param genome_version:
    :param output_format:
    :return:
    """

    if annotate is not None:
        annotate_qid(qid, annotate, genome_version=genome_version, data_dir=data_dir)

    # load saved file
    bframe = load_file(qid, data_dir, start_row=start_row, end_row=end_row)
    max_rows = bframe.max_variants

    column_defs = []
    table_data = []

    if output_format == "vcf":
        table_data = []

        for var in bframe.data.keys():
            # base VCF columns
            if "variant_data" in bframe.data[var]:
                if "ID" in bframe.data[var]["variant_data"]:
                    id_data = bframe.data[var]["variant_data"]['ID']
                else:
                    id_data = "."

                if "QUAL" in bframe.data[var]["variant_data"]:
                    qual_data = bframe.data[var]['variant_data']['QUAL']
                else:
                    qual_data = '.'

                if "FILTER" in bframe.data[var]["variant_data"]:
                    filter_data = bframe.data[var]['variant_data']['FILTER']
                else:
                    filter_data = '.'

            #print(bframe.data[var])

            dc = {
                'chrom': bframe.data[var]["variant_data"]["CHROM"],
                'pos': bframe.data[var]["variant_data"]["POS"],
                'id': id_data,
                'ref': bframe.data[var]["variant_data"]["REF"],
                'alt': bframe.data[var]["variant_data"]["ALT"],
                'qual': qual_data,
                'filter': filter_data
            }
            column_defs = [
                {'headerName': 'CHROM', 'field': 'chrom', 'filter': "agTextColumnFilter", 'floatingFilter': 'true','minWidth': 200},
                {'headerName': 'POS', 'field': 'pos', 'filter': "agNumberColumnFilter", 'floatingFilter': 'true','minWidth': 200},
                {'headerName': 'ID', 'field': 'id', 'filter': 'agTextColumnFilter', 'floatingFilter': 'true','minWidth': 200},
                {'headerName': 'REF', 'field': 'ref', 'filter': "agTextColumnFilter", 'floatingFilter': 'true','minWidth': 200},
                {'headerName': 'ALT', 'field': 'alt', 'filter': "agTextColumnFilter", 'floatingFilter': 'true','minWidth': 200},
                {'headerName': 'QUAL', 'field': 'qual', 'filter': 'agNumberColumnFilter', 'floatingFilter': 'true','minWidth': 200},
                {'headerName': 'FILTER', 'field': 'filter', 'filter': 'agTextColumnFilter', 'floatingFilter': 'true','minWidth': 200}
            ]

            # Preexisting features
            #print(bframe.data)
            info_features = bframe.data[var]["info_features"].keys()
            #print(bframe.data[var]["info_features"])
            for inf in info_features:
                column_type = recognize_column_types([bframe.data[var]["info_features"][inf]])
                if column_type == "float":
                    filter_type = "agNumberColumnFilter"
                elif column_type == "integer":
                    filter_type = "agNumberColumnFilter"
                else:
                    filter_type = "agTextColumnFilter"

                dc[inf.lower()] = bframe.data[var]["info_features"][inf]

                inf_column = { 'headerName': inf, 'field': inf.lower(), 'filter': filter_type, 'floatingFilter': 'true',
                               'minWidth': 200}
                column_defs.append(inf_column)

            table_data.append(dc)


    else:

        table_data = [
            {'id': 1, 'name': 'John Doe', 'age': 28, 'country': 'USA'},
            {'id': 2, 'name': 'Jane Smith', 'age': 34, 'country': 'Canada'},
            {'id': 3, 'name': 'Sam Green', 'age': 45, 'country': 'UK'},
        ]

        column_defs = [
            {'headerName': 'ID', 'field': 'id', 'minWidth': 200},
            {'headerName': 'Name', 'field': 'name'},
            {'headerName': 'Age', 'field': 'age'},
            {'headerName': 'Country', 'field': 'country'},
        ]


    return column_defs, table_data, max_rows

def analyze_search():

    column_defs = []
    table_data = []

    return column_defs, table_data

