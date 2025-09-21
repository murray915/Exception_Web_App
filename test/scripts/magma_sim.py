from icecream import ic
import file_mgnr as fm
import datetime, time, os, json
import random as rd
import threading as thr


def addSecs(tm, secs) -> time:
    """ Add input seconds to timestamp """
    fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + datetime.timedelta(seconds=secs)
    return fulldate.time()


def runset(dest: str, src: str, runtime:time, fileexnt: str, sys_drain_rate: int):
    """
    dest: destination path for files to end at
    src: source path for files to pull from
    runtime: lifetime of process
    fileexnt: pattern in filename to lookfor in source dir
    """

    try:
        # general params
        sys_drain_rate += rd.uniform(0,0.8)

        # main loop
        while datetime.datetime.now().time() < runtime:

            # start collection HTTP > Sales_Orders
            if not os.listdir(dest) and os.listdir(src):
                ic("Runset started - ",fileexnt)
                fm.move_dir(src,dest,0,"*"+fileexnt+"*")

            # drain Sales_Orders
            if os.listdir(dest):
                ic('File deleted from: ',fileexnt)
                time.sleep(sys_drain_rate)                       
                fm.move_dir(dest,root+'/magma/magma_in/BIN',1,"*"+fileexnt+"*")

        return True
    
    except Exception as err: # Exception Block. Return data to user & False
        ic(f"** Unexpected {err=}, {type(err)=} **")
        fm.delete_magma_folder(root)
        return False



def magma_run(runtime: int, root: str, sys_drain_rate: int, sys_create_rate: int) -> bool:
    """
    runtime: total (sec) for simulation
    root: "./test/" top path to create "\magma\..." within
    sys_drain_rate: rate of subfolder clearance
    sys_create_rate: rate of file creation per heartbeat (max per, avg between /2 and input)

    return True/False on completion
    """

    try:       
        # gen params
        fm.create_magma_folder(root)
        app_runtime = post_interval = addSecs(datetime.datetime.now().time(), runtime)
        counter = 1
        processes = []

        with open(".\data\console_settings.json", mode="r", encoding="utf-8") as read_file:
            settings_data = json.load(read_file)
            interval = int(settings_data["heartbeat_rate"][2])

        runset_gen = [
            [root+'/magma/magma_in/Sales_Orders',root+'/magma/magma_recv/HTTP-IN',app_runtime,'SAOR',sys_drain_rate],
            [root+'/magma/magma_in/Priority_Sales_Orders',root+'/magma/magma_recv/HTTP-IN',app_runtime,'SAPR',sys_drain_rate],
            [root+'/magma/magma_in/Customers',root+'/magma/magma_recv/HTTP-IN',app_runtime,'SUPR',sys_drain_rate]
        ]
        
        # create runsets
            # duration of the app runtime
        for i, run in enumerate(runset_gen):
            i = thr.Thread(target=runset, args=(*run,))
            i.start()
            processes.append(i)

        # http/file creation loop
        while datetime.datetime.now().time() < app_runtime:

            # generat HTTP-IN files
            if post_interval < datetime.datetime.now().time() or counter == 1:
                ic("File Generation Started:")
                
                # update params
                post_interval = addSecs(datetime.datetime.now().time(), interval)

                for runsets in runset_gen:
                    add_files = int(rd.randrange(sys_create_rate/2,sys_create_rate))
                    fm.create_xmls(runsets[1], add_files, counter, runsets[3])
                    counter += add_files

                ic("Next interval: ",post_interval)
                ic("Current counter: ",counter)


        # cleanup
        for p in processes:
            p.join()

        fm.delete_magma_folder(root)
        
        return True

    except Exception as err: # Exception Block. Return data to user & False
        ic(f"** Unexpected {err=}, {type(err)=} **")
        fm.delete_magma_folder(root)
        return False


if __name__ == '__main__':

    root = "C:/Users/Murray/Downloads"
    runtime = 360
    sys_drain_rate = 1.6
    sys_create_rate = 20
    interval = 30

    def heartbeat(runtime: time, root: str):
        app_runtime = addSecs(datetime.datetime.now().time(), runtime)
        post_interval = datetime.datetime.now().time()
        outputlist = []

        # http/file creation loop
        while datetime.datetime.now().time() < app_runtime:

            # generat HTTP-IN files
            if post_interval < datetime.datetime.now().time():

                # update params
                post_interval = addSecs(datetime.datetime.now().time(), 60)                
                files = fm.list_files(root+"/magma/magma_in/Sales_Orders")
                outputlist.append([datetime.datetime.now().time().strftime('%H:%M'),len(files)])

                ic('---------- Heartbeat Stats ---------- ',
                    outputlist)


    app_run = thr.Thread(target=magma_run, args=(runtime, root, sys_drain_rate, sys_create_rate))
    app_run.start() 

    heartbeat_run = thr.Thread(target=heartbeat, args=(runtime, root))
    heartbeat_run.start()