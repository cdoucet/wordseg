#ifndef _DATA_CORPUS_HH
#define _DATA_CORPUS_HH

#include "data/data.hh"

namespace data
{
    class corpus_data: public data
    {
    public:
        corpus_data();
        virtual ~corpus_data();

        virtual void read(std::wistream& is, U start, U ns);

        // read additional data for evaluation
        void read_eval(std::wistream& is, U start, U ns);

        virtual std::vector<Sentence> get_eval_sentences() const;

        void initialize(U ns);

    private:
        U _evalsent_start;  // sentence # of first eval sentence

        void read_data(std::wistream& is, U start, U ns);
    };
}

#endif  // _DATA_CORPUS_HH