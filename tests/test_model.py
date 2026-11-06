import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from trade_model import allocate

class ModelTests(unittest.TestCase):
    def setUp(self): self.w=(0.02,0.22,0.76)
    def test_baseline(self):
        a=allocate(self.w,4)
        self.assertEqual(a.shares,self.w)
        self.assertAlmostEqual(a.price_index,1)
        self.assertAlmostEqual(a.tariff_revenue,0)
    def test_accounting_and_diversion(self):
        a=allocate(self.w,4,(0,0.25,0))
        self.assertAlmostEqual(sum(a.customs)+a.tariff_revenue,100)
        self.assertAlmostEqual(sum(a.shares),1)
        self.assertGreater(a.shares[0],self.w[0])
        self.assertLess(a.shares[1],self.w[1])
        self.assertGreater(a.price_index,1)
    def test_uniform_price_scaling(self):
        a=allocate(self.w,4,costs=(2,2,2))
        self.assertEqual(a.shares,self.w)
        self.assertAlmostEqual(a.price_index,2)
    def test_uniform_tariffs(self):
        a=allocate(self.w,4,(0.1,0.1,0.1))
        for x,y in zip(a.shares,self.w): self.assertAlmostEqual(x,y)
        self.assertAlmostEqual(a.price_index,1.1)
        self.assertAlmostEqual(a.tariff_revenue,100/11)
    def test_cost_penalty(self):
        a=allocate(self.w,4,(0,0.25,0))
        b=allocate(self.w,4,(0,0.25,0),(1.1,1,1))
        self.assertLess(b.customs[0],a.customs[0])
    def test_invalid_inputs(self):
        for kwargs in [{'sigma':1},{'sigma':float('nan')},{'sigma':4,'costs':(0,1,1)},{'sigma':4,'tariffs':(-1,0,0)}]:
            with self.assertRaises(ValueError): allocate(self.w,**kwargs)

if __name__=='__main__': unittest.main()
