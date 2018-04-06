#include "estimator/viterbi.hh"


estimator::batch_unigram_viterbi::batch_unigram_viterbi(
    const parameters& params, const corpus::corpus_base& corpus, const annealing& anneal)
    : batch_unigram(params, corpus, anneal)
{}

estimator::batch_unigram_viterbi::~batch_unigram_viterbi()
{}

void estimator::batch_unigram_viterbi::estimate_sentence(sentence& s, double temperature)
{
    s.erase_words(m_lex);
    s.maximize(m_lex, m_corpus.nsentences()-1, temperature, m_params.do_mbdp());
    s.insert_words(m_lex);
}


estimator::batch_bigram_viterbi::batch_bigram_viterbi(
    const parameters& params, const corpus::corpus_base& corpus, const annealing& anneal)
    : batch_bigram(params, corpus, anneal)
{}

estimator::batch_bigram_viterbi::~batch_bigram_viterbi()
{}

void estimator::batch_bigram_viterbi::estimate_sentence(sentence& s, double temperature)
{
    s.erase_words(m_lex);
    s.maximize(m_lex, m_corpus.nsentences()-1, temperature);
    s.insert_words(m_lex);
}




estimator::online_unigram_viterbi::online_unigram_viterbi(
    const parameters& params, const corpus::corpus_base& corpus, const annealing& anneal, double forget_rate)
    : online_unigram(params, corpus, anneal, forget_rate)
{}

estimator::online_unigram_viterbi::~online_unigram_viterbi()
{}

void estimator::online_unigram_viterbi::estimate_sentence(sentence& s, double temperature)
{
    s.maximize(m_lex, m_nsentences_seen, temperature, m_params.do_mbdp());
    s.insert_words(m_lex);
}


estimator::online_bigram_viterbi::online_bigram_viterbi(
    const parameters& params, const corpus::corpus_base& corpus, const annealing& anneal)
    : online_bigram(params, corpus, anneal)
{}

estimator::online_bigram_viterbi::~online_bigram_viterbi()
{}

void estimator::online_bigram_viterbi::estimate_sentence(sentence& s, double temperature)
{
    s.maximize(m_lex, m_nsentences_seen, temperature);
    s.insert_words(m_lex);
}