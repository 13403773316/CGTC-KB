# Chinese Government Text Correction with Knowledge Bases

## Task Introduction

Chinese Text Correction has gone through rapid development in recent years, with machine learning-based correction algorithms significantly improving the performance. However, current studies normally lack considerations on the use of knowledge bases to instruct the correction, while knowledge bases could be helpful in correcting key factual errors or adjusting the correction results with respect to the changes in the knowledge bases. We have developed a dataset and knowledge bases specifically for the automatic text correction of government documents based on real user inputs. The "Chinese Government Text Correction with Knowledge Bases" shared task aims to enhance Chinese text correction with the help of knowledge bases, and to test the effectiveness of various methods in utilizing knowledge bases.

## Data Description & Rules

We provide a Chinese grammatical error correction benchmark named CGTC_KB, which focuses on correcting errors in Chinese government texts. In this task, the benchmark data is divided into three parts: training set, validation set, and test set.

**Data Description:**

- Training Set (train.txt and train.kb.jsonl): a synthetic data, collected by extracting sentences which can trigger KB matching from a large news crawl corpus, providing both the extracted sentences and corresponding matched KB elements.
- Validation Set (dev.input.txt, dev.kb.jsonl and ref.dev.txt): collected from real user inputs, containing original sentences, matched KB elements and the corrected sentences. The validation set can be used for model performance testing and hyper-parameter tuning, but it cannot be directly used for model training.
- Test Set (test.input.txt and test.kb.jsonl): collected from real user inputs, containing original sentences and matched KB elements. The correction results are held out by the organizers for evaluation. Participants are required to submit the correction results of their systems.

The data can be found at  [this link](https://pan.baidu.com/s/1V03Fa08hB-3vvzuhgYwHCQ?pwd=2002).

**Rules:**

For model training, only [Lang8](http://tcci.ccf.org.cn/conference/2018/taskdata.php), [HSK](https://cloud.tsinghua.edu.cn/f/9e46b10b52564736b0f3/),  [CGED](https://github.com/blcuicall/cged_datasets), [MuCGEC](https://github.com/HillZhang1999/MuCGEC), [YACLC](https://github.com/blcuicall/YACLC) and [CTC2021](https://github.com/destwang/CTC2021) and [NaCGEC](https://dgithub.xyz/masr2000/NaCGEC) are allowed to be used as additional supervised data (i.e., parallel data). When using these datasets, please follow the rules set by the original data publishers.
Additionally, for unsupervised data, any publicly available corpus on the web is allowed. Based on unsupervised data, participants can use any data augmentation methods to construct pseudo-parallel data for model training.

## Submission & Evaluation

For submission, the following materials should be packaged as one `zip` file and sent to [songyang_1120@qq.com]:

- Submission File: The output sentences should be written into one text file. **The format of submission file must be the same as the input file. Specifically, the submission file must contain the same number of lines as the input file, and each line is a correct sentence corresponding to the sentence in the input file.** 
- Document:
  - Data Description: The document needs to contain a brief description of supervised and unsupervised data used in the experiment, as well as the data augmentation methods for unsupervised data.
  - Sharing Link of Unsupervised Data: Unsupervised data used in the experiment should be uploaded to a cloud storage, i.e., net disk, and the sharing link should be included in the document. It is not allowed to use data that violates the rules during model training.
- Code[optional]: The code folder should contain all the codes of data augmentation, data processing, model training and model inference.

**For evaluation**, we evaluate with Precision, Recall and $\text{F}_{0.5}$ between the output sentence and gold edits, as well as the correction accuracy and miscorrection probability w.r.t. the KB elements.

## Contact 

If you have any questions about this task, please email to [songyang_1120@qq.com].
