import cPickle

data = cPickle.load(open(r'../Pre-trained/srnn_smoking/checkpoint.pik'))
data['model'] = data[0]
data['label'] = data[1]
for model, label in zip(data[0], data[1]):
    print model
    print label
    

