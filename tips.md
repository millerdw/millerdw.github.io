---
layout: page
title: Tips for Data Science
permalink: /tips/
---

### Data Exploration - VET your beliefs

In Data Exploration we want to bootstrap our understanding of the dataset at hand. I like to think in terms of VET (Visualise-Explain-Test): 
- **Visualise:** Wrangle your data and plot it in the most meaningful ways. Really, just get your hands dirty with it, plot everything.
- **Explain:** Given the patterns that appear in the data and your priors of the domain, can you build a hypothesis to explain the data? 
- **Test:** This is the important part, cross-referencing your beliefs. Can you prove or disprove your hypothesis using additional data or following them to their logical conclusions?

This process takes the form of a loop; start with a dataset and a set of priors (beliefs) about that data, Visualise a new piece of information from the dataset, Explain the patterns by choosing a hypothesis, and Test it using an alternative dataset. If the Hypothesis is *proved* correct or incorrect, use it to update your beliefs. If it is not *proved* correct or incorrect, test it again.

In this way, given a reasonable dataset, you will bootstrap your priors into a more accurate or more confident set of beliefs.



### Time Series Data - Lies, Damn Lies, and Cumulative Growth Statistics

It's not immediately obvious, but cumulative growth statistics - for example annualised returns or compound annual growth rate - are the work of the devil.

There are a couple of things to really look out for when analysing 
- **Start Date:** Why did the collector of this statistic pick the start date, is it different to other metrics?
- **Survivorship Bias:** What's happened to examples of negative annualised returns? Are they being reported or have they been forgotten?








