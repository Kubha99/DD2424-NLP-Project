from utils import read_data
import torch
import pandas as pd
import lstm
import rnn
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == '__main__':
    data_dict = read_data()
    train_text = data_dict["train_text"]
    test_text = data_dict["test_text"]
    index2char = data_dict["index2char"]
    char2index = data_dict["char2index"]

    DIR = "../results/rnn_vs_lstm"
    SEQUENCE_LENGTH = 25
    BATCH_SIZE = 1
    NUM_EPOCHS = 100000
    HIDDEN_SIZE = 100
    NUM_LAYERS = 2
    TEMPERATURE = 0.29
    LEARNING_RATE = 0.01
    LABEL_SMOOTHING = 0

    rnn_gen =  rnn.Generator(
        input_string=train_text,
        test_string=test_text, 
        index2char=index2char, 
        char2index=char2index,
        sequence_length=SEQUENCE_LENGTH,
        batch_size=BATCH_SIZE
        )

    rnn_model =  rnn.RNN(
        input_size=len(index2char), 
        hidden_size=HIDDEN_SIZE, 
        num_layers=NUM_LAYERS, 
        output_size=len(index2char),
    ).to(rnn_gen.device)

    rnn_gen.train(
        rnn=rnn_model,
        num_epchs=NUM_EPOCHS,
        print_every=500,
        lr=LEARNING_RATE,
        temperature=TEMPERATURE,
        label_smoothing=LABEL_SMOOTHING,
    )
    
    """
    Save RNN model
    """
    torch.save(rnn_model.rnn.state_dict(), f"{DIR}/rnn_hidden{HIDDEN_SIZE}_epoch{NUM_EPOCHS}_lr{LEARNING_RATE}_nlayer{NUM_LAYERS}.pth")
    rnn_df = pd.DataFrame(rnn_gen.history)
    rnn_df.to_csv(f"{DIR}/rnn_hidden{HIDDEN_SIZE}_epoch{NUM_EPOCHS}_lr{LEARNING_RATE}_nlayer{NUM_LAYERS}.csv", index=False) 

    sns.set_style("whitegrid")
    title_string = f"RNN: Loss vs iterations\nHidden Layers:{HIDDEN_SIZE}, lr:{LEARNING_RATE}"
    rnn_fig = sns.lineplot(data=rnn_df, x="iterations", y="loss")
    rnn_fig.get_figure().savefig(f'{DIR}/rnn_hidden{HIDDEN_SIZE}_epoch{NUM_EPOCHS}_lr{LEARNING_RATE}_nlayer{NUM_LAYERS}.png')
    
    

    # lstm_gen = lstm.Generator(
    #     input_string=train_text,
    #     test_string=test_text,
    #     index2char=index2char, 
    #     char2index=char2index,
    #     sequence_length=SEQUENCE_LENGTH,
    #     batch_size=BATCH_SIZE
    #     )

    # lstm_model = lstm.RNN(
    #     input_size=len(index2char), 
    #     hidden_size=HIDDEN_SIZE, 
    #     num_layers=NUM_LAYERS, 
    #     output_size=len(index2char),
    # ).to(lstm_gen.device)

    # lstm_gen.train(
    #     lstm=lstm_model,
    #     num_epchs=NUM_EPOCHS,
    #     print_every=500,
    #     lr=LEARNING_RATE,
    #     temperature=TEMPERATURE,
    #     label_smoothing=LABEL_SMOOTHING,
    # )


    """
    Save LSTM model
    """
    # torch.save(lstm_gen.lstm.state_dict(), f"{DIR}/lstm_hidden{HIDDEN_SIZE}_epoch{NUM_EPOCHS}_lr{LEARNING_RATE}_nlayer{NUM_LAYERS}.pth")
    # lstm_df = pd.DataFrame(lstm_gen.history)
    # lstm_df.to_csv(f'{DIR}/lstm_hidden{HIDDEN_SIZE}_epoch{NUM_EPOCHS}_lr{LEARNING_RATE}_nlayer{NUM_LAYERS}.csv', index=False) 

    # sns.set_style("whitegrid")
    # title_string = f"LSTM: Loss vs iterations\nHidden Layers:{HIDDEN_SIZE}, lr:{LEARNING_RATE}"
    # lstm_fig = sns.lineplot(data=lstm_df, x="iterations", y="loss")
    # lstm_fig.get_figure().savefig(f'{DIR}/lstm_hidden{HIDDEN_SIZE}_epoch{NUM_EPOCHS}_lr{LEARNING_RATE}_nlayer{NUM_LAYERS}.png')
    """
    To load model to cuda but it was saved on cpu (or vice versa) use:
    device = torch.device("cuda")
    lstm = lstm.RNN(*args, **kwargs)
    lstm.load_state_dict(torch.loadc(PATH, map_location=device))
    """
