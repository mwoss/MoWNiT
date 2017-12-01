#include <stdlib.h>
#include <gsl/gsl_math.h>
#include <gsl/gsl_monte.h>
#include <gsl/gsl_monte_plain.h>
#include <gsl/gsl_monte_miser.h>
#include <gsl/gsl_monte_vegas.h>

//funkcja x^2
double
g (double *k, size_t dim, void *params)
{
    return k[0]*k[0];
}

void
display_results (char *title, double result, double error)
{
    printf ("%s ==================\n", title);
    printf ("result = % .6f\n", result);
    printf ("error  = % .6f\n", error);
}

int
main (void)
{
    double res, err;
    double xl[2] = { 0, 0}; //najmniejsze wartosci
    double xu[2] = { 1,1 }; //najwiesze wartosci
    const gsl_rng_type *T;
    gsl_rng *r;
    gsl_monte_function G = { &g, 2, 0 };
    FILE *p,*m,*v;
    p= fopen("p.txt", "w");
    m= fopen("m.txt", "w");
    v= fopen("v.txt", "w");


    for(int i=100; i<10000;i++) {
        size_t calls = i; // liczba wywolan funkcji
        gsl_rng_env_setup();
        T = gsl_rng_default;
        r = gsl_rng_alloc(T);
        {
            gsl_monte_plain_state *s = gsl_monte_plain_alloc(2);
            gsl_monte_plain_integrate(&G, xl, xu, 2, calls, r, s, &res, &err);
            gsl_monte_plain_free(s);
            fprintf(p, "%d\t\t\t", calls);
            fprintf(p, "%f \n", err);
          //  display_results("plain", res, err);
        }
        {
            gsl_monte_miser_state *s = gsl_monte_miser_alloc(2);
            gsl_monte_miser_integrate(&G, xl, xu, 2, calls, r, s, &res, &err);
            gsl_monte_miser_free(s);
            fprintf(m, "%d\t\t", calls);
            fprintf(m, "%f \n", err);
          //  display_results("miser", res, err);
        }
        { gsl_monte_vegas_state *s = gsl_monte_vegas_alloc(2);
          gsl_monte_vegas_integrate(&G, xl, xu, 2, calls , r, s,&res, &err);
           display_results("vegas final", res, err);
            fprintf(v, "%d\t\t", calls);
            fprintf(v, "%f \n", err);
            gsl_monte_vegas_free(s);
        }
    }
    gsl_rng_free (r);

    return 0;
}