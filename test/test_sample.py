
import unittest
from extra import ProcessQueue
import json


class MyTest(unittest.TestCase):



    def test(self):

        qObject = ProcessQueue() #queue object
        mData = json.loads(qObject.getMeta() )
        mFmsg = json.loads( qObject.getFullMessage() )

        self.assertEqual(mData["meta"]["code"], 200)
        self.assertEqual( len(mFmsg["data"]), 10)


if __name__ == '__main__':
    unittest.main()

