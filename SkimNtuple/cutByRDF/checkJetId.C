#include <iostream>
#include <cmath>

#include "TMath.h"

void checkJetId(int year)
{
	using namespace std;
	float jetNumConst = 2;
	float jetNEMF = .89;
	float jetMUF = 0.7;
	float jetNHF = 0.8;
	double jetEta = -2.7;
	float jetCEMF = .1;
	float jetCHM = 1;
	float jetCHF = 1;

	if (year == 2018) 
	{
		bool jetID = jetNumConst > 1 && jetNEMF < 0.9 && jetMUF < 0.8 && jetNHF < 0.9 && fabs(jetEta) <= 2.6 && jetCEMF < 0.8 && jetCHM > 0 && jetCHF > 0;
		cout << jetID << endl;
	}
	else if (year == 2017) 
	{
		bool jetID = (jetNumConst > 1 && jetNEMF < 0.9 && jetMUF < 0.8 && jetNHF < 0.9 && fabs(jetEta) <= 2.7) && (fabs(jetEta) > 2.4 || (fabs(jetEta) <= 2.4 && jetCEMF < 0.8 && jetCHM > 0 && jetCHF > 0));
		cout << jetID << endl;
	}
	else if (year == 2016) 
	{
		bool jetID = (jetNEMF < 0.99 && jetNHF < 0.9 && fabs(jetEta) <= 2.7) && (fabs(jetEta) > 2.4 || (fabs(jetEta) <= 2.4 && jetCEMF < 0.8 && jetCHM > 0 && jetCHF > 0 && jetNumConst > 1 && jetMUF < 0.8 && jetNEMF < 0.9));
		cout << jetID << endl;
	}
	else if (year == 2015) 
	{
		bool jetID = (jetNHF < 0.90 && jetNEMF < 0.90 && jetNumConst > 1 && jetMUF < 0.8) && ((fabs(jetEta) <= 2.4 && jetCHF > 0 && jetCHM > 0 && jetCEMF < 0.90) || fabs(jetEta) > 2.4) && fabs(jetEta) <= 2.7;
		cout << jetID << endl;
	}
}