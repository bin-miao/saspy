import unittest
import saspy


class TestSASsessionObject(unittest.TestCase):
    def __init__(self, *args):
        super(TestSASsessionObject, self).__init__(*args)
        self.sas = saspy.SASsession()#cfgname='default')
        self.assertIsInstance(self.sas, saspy.SASsession, msg="sas = saspy.SASsession(...) failed")

    def __del__(self, *args):
        if self.sas:
           self.sas._endsas()

    def setUp(self):
        #self.sas = saspy.SASsession()
        pass

    def tearDown(self):
        #if self.sas:
        #   self.sas._endsas()
        pass

    def test_SASsession(self):
        #test exist true
        exists = self.sas.exist('cars', libref='sashelp')
        self.assertTrue(exists, msg="exists = self.sas.exist(...) failed")

        #test exist false
        self.sas.set_batch(True)
        exists = self.sas.exist('notable', libref='sashelp')
        self.assertFalse(exists, msg="exists = self.sas.exist(...) failed")

        #test sasdata existing
        self.cars = self.sas.sasdata('cars', libref='sashelp', results='text')
        self.assertIsInstance(self.cars, saspy.SASdata, msg="cars = sas.sasdata(...) failed")

        #test sasdata not existing
        self.notable = self.sas.sasdata('notable', results='text')
        self.assertIsInstance(self.cars, saspy.SASdata, msg="cars = sas.sasdata(...) failed")

        #test create non-existing table
        ll = self.sas.submit("data notable;x=1;run;")
        exists = self.sas.exist('notable')
        self.assertTrue(exists, msg="exists = self.sas.exist(...) failed")

        #test write and read csv
        self.sas.set_batch(True)
        log = self.sas.write_csv('/tmp/sas_csv_test.csv', 'cars', libref='sashelp')
        self.assertNotIn("ERROR", log, msg="sas.write_csv() failed")
        csvdata = self.sas.read_csv('/tmp/sas_csv_test.csv', 'csvcars', results='text')
        ll = csvdata.head()
        expected = ['1', 'Acura', 'MDX', 'SUV', 'Asia', 'All', '$36,945', '$33,337', '3.5']
        rows = ll['LST'].splitlines()
        retrieved = []
        for i in range(len(rows)):
           retrieved.append(rows[i].split())
        self.assertIn(expected, retrieved, msg="csvcars.head() result didn't contain row 1")
        
        #test datasets()
        self.sas.set_batch(True)
        log = self.sas.datasets()
        expected = ['Libref', 'WORK']
        rows = log.splitlines()
        retrieved = []
        for i in range(len(rows)):
           retrieved.append(rows[i].split())
        self.assertIn(expected, retrieved, msg="cars.datasets() result didn't contain expected result")

        log = self.sas.datasets('sashelp')
        expected = ['Libref', 'SASHELP']
        rows = log.splitlines()
        retrieved = []
        for i in range(len(rows)):
           retrieved.append(rows[i].split())
           if i > 20:
              break  #it'll be in the first 20 rows for sure. don't need all of it
        self.assertIn(expected, retrieved, msg="cars.datasets(...) result didn't contain expected result")
        
        #test stat
        stat = self.sas.sasstat()
        self.assertIsInstance(stat, saspy.SASstat, msg="stat = self.sas.sasstat() failed")

        #test ets
        ets = self.sas.sasets()
        self.assertIsInstance(ets, saspy.SASets, msg="ets = self.sas.sasets() failed")

        #test stat
        qc = self.sas.sasqc()
        self.assertIsInstance(qc, saspy.SASqc, msg="qc = self.sas.sasqc() failed")

        #test stat
        ml = self.sas.sasml()
        self.assertIsInstance(ml, saspy.SASml, msg="ml = self.sas.sasml() failed")
