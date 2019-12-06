#!/usr/bin/python3 
def ingest_log_stream(event, context):  
    """Extract time/memory logistics for Lambda
       to keep track of memory/time usage vs data size
    :param event: the event that triggered this lambda
    :param context: context associated to the lambda
    :return: display memory limits, time spent and remaining
    """
    print("Mem. limits(MB):", context.memory_limit_in_mb)
    time.sleep(1)

    #print("Time remaining (MS):", context.get_remaining_time_in_millis())
    msconsumed = 900000 - context.get_remaining_time_in_millis()
    msconstime = msconsumed * 1/6000.0
    print("Consumed (Minutes) ",msconstime)
    timeremain = 15.0 - msconstime
    print("Time remaining in Minutes ", timeremain)
    return str(mconstime)
                  
def ingest_size_string(fsiz):
    """Create a formatted size based on the number
    :param fsiz: in Bytes the size of content
    :return: formatted either in KB, MB, GB depending on the size.
    """
    sizes = [ "B", "KB", "MB", "GB", "TB" ]
    order = 0
    #drill down to the level of data size
    while (fsiz >= 1024 and order < len(sizes) - 1):
        order += 1
        fsiz = fsiz/1024
    result = "{0:.2f} {1}".format(fsiz, sizes[order])
    return result

def ingest_getpackagename(fname):
    """Clean package name for special case (tar.gz and tar)
    :param fname: file name - determines the cleanup
   :return: .tar or .gz
    """
    if fname.endswith(".tar.gz"):
        return fname.replace('.gz','')
    elif fname.endswith(".tgz"):
        return fname.replace('.tgz','.tar')
    else:
        return fname

def ingest_getcontenttype(str):
    if str.find('application/') > -1: 
       pos = str.find('application/')+len('application/')
       retval = str[pos:]
       if retval == 'x-gzip' or retval == 'x-tar':
          return 'tgz'
       else:
          return retval
