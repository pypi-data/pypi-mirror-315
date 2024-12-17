# This code is for converting xpt file to csv file
# -----------------------------------------------------------------------------
# Date                     Programmer
# ----------   --------------------------------------------------------------
# Jan-10-2024    Md Yousuf Ali (md.ali@fda.hhs.gov)
#
#
import pathlib
import pyreadstat
import click

@click.command()
@click.argument("xpt_path")
@click.argument("where_to_save")
def xpt_to_csv(xpt_path, where_to_save):
    """
    this code is for converting xpt file to csv file

    """

    if pathlib.Path(xpt_path).is_file():
        df, meta = pyreadstat.read_xport(xpt_path)
        file_name = pathlib.Path(xpt_path).stem
        file_name = file_name + '.csv'
        path_to_save = pathlib.Path(where_to_save, file_name)
        df.to_csv(path_to_save)
    else:

        if pathlib.Path(xpt_path).is_dir():
            path_x = pathlib.Path(xpt_path)
            all_xpt = [i for i in path_x.rglob('*.xpt')]
            unq_dir = set([i.parent.name for i in all_xpt])
            # breakpoint()
            dir_save = []
            for i in unq_dir:
                k = pathlib.Path(where_to_save, i)
                if k not in dir_save:
                    dir_save.append(k)
                k.mkdir(exist_ok=True)
            for i in all_xpt:
                file_name = i.stem + '.csv'
                try:
                    df, meta = pyreadstat.read_xport(i)
                    final_path = i.parent.name

                    save_to = pathlib.Path(where_to_save, final_path, file_name)
                    df.to_csv(save_to)
                except:
                    # print(i)
                    click.echo(i)

if __name__=="__main__":
    xpt_to_csv()






# xpt_to_csv(xpt_path= phuse_xpt, where_to_save= save_file )


