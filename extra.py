import boto3
import json


class ProcessQueue:
    'Common base for queue'
    __sqs = None
    __queue = None
    __totalMsg = None
    __version = 1.2
    __maxNumOfMessages = 0
    __errormsg =    {
                        200: "success",
                        404: "failure"
                    }

    def __init__(self, qName='challenge-backend', maxNumOfMessages = 10 ):
        '''
            Constructor
        '''
        # Get the service resource
        self.__sqs = boto3.resource('sqs')
        # Get the queue
        self.__queue = self.__sqs.get_queue_by_name(QueueName=qName)

        #maximum number of elements in queue
        self.__maxNumOfMessages = maxNumOfMessages

   
    def getMeta(self):
        '''
            metadata in json
        '''
        status = 404

        # check if any element in queue
        isempty = len (self.__queue.receive_messages(MaxNumberOfMessages=1)) == 0        
        if not isempty:
            status = 200
            successDict = {
              "meta": {
                "code": status
              },
              "version": self.__version
            }
            return json.dumps(successDict, ensure_ascii=False)

        failureDict = {
          "meta": {
            "code": status,
            "error": self.__errormsg[status]
          }
        }
        return json.dumps(failureDict, ensure_ascii=False)



    def getFullMessage(self):
        '''
            The full message in json
        '''
        outputData = []
        status = 404
        dataCnt = 0
        # Get messages in queue
        for message in self.__queue.receive_messages(MaxNumberOfMessages=self.__maxNumOfMessages):
            # process message body
            outputData.append(message.body)
            dataCnt = dataCnt + 1
            message.delete()

        if (dataCnt > 0):
            status = 200
            output = {
              "meta": {
                "code": status
              },
              "data": outputData,
              "count": dataCnt
            }
            return json.dumps(output, ensure_ascii=False)

        failureDict = {
          "meta": {
            "code": status,
            "error":  self.__errormsg[status]
          }
        }
        return json.dumps(failureDict, ensure_ascii=False)
