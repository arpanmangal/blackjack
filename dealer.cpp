#include <iostream>
#include <fstream>
using namespace std;

double prob;
double probability[10][7];

int busted_cutoff = 21;
int dealer_cutoff = 17;

int eval_prob(int dealer_sum, int num_cards, bool is_soft, double acc_prob, int face_up) {
    // cout << "Starting for " << dealer_sum << " and " << face_up << endl;
    cout << "Accumulated Probability " << acc_prob << endl;
    if (dealer_sum > busted_cutoff) {
        if (is_soft) {
            eval_prob(dealer_sum-10, num_cards, false, acc_prob, face_up);
        } else {
            probability[face_up-2][22-17] += acc_prob;
            cout << "Change at " << face_up << " 22 " << acc_prob << " " << probability[face_up-2][5] << endl;
        }
    } else if (dealer_sum == busted_cutoff && num_cards == 2) {
        cout << "Change at " << face_up << " 23 " << acc_prob << " " << probability[face_up-2][6] << endl;
        probability[face_up-2][23-17] += acc_prob;
    } else if (dealer_sum >= dealer_cutoff) {
        cout << "Change at " << face_up << " " << dealer_sum << " " << acc_prob << " " << probability[face_up-2][dealer_sum-17] << endl;
        probability[face_up-2][dealer_sum-17] += acc_prob;
    } else {
        for(int card = 2; card < 12; card++) {
            if (card == 10) {
                eval_prob(dealer_sum+card, num_cards+1, is_soft, acc_prob*prob, face_up);
            } else if (card == 11) {
                eval_prob(dealer_sum+card, num_cards+1, true, acc_prob*(1-prob)/9, face_up);
            } else {
                eval_prob(dealer_sum+card, num_cards+1, is_soft, acc_prob*(1-prob)/9, face_up);
            }
        }
    }

    return 0;
}

int generate_table() {
    for (int card =  2; card < 12; card++) {
        if (card == 11) {
            eval_prob(card, 1, true, 1, 11);
        } else {
            eval_prob(card, 1, false, 1, card);
        }
    }

    return 0;
}

int write_table() {
    ofstream outfile;
    outfile.open("stand.prob");

    for (int card = 2; card < 12; card++) {
        for (int dsum = 17; dsum < 24; dsum++) {
            outfile << probability[card-2][dsum-17] << " ";
        }
        outfile << endl;
    }

    return 0;
}

int main(int argc, char const *argv[])
{
    prob = stod(argv[1]);
    cout << prob << endl;
    generate_table();

    write_table();
    return 0;
}
