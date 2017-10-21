//+------------------------------------------------------------------+
//|                                            BinaryOptionTrade.mqh |
//|                                                    Ricardo Lucca |
//|                                        http://github.com/~rlucca |
//+------------------------------------------------------------------+
#property copyright "Ricardo Lucca"
#property link      "http://github.com/~rlucca"
#property strict
//+------------------------------------------------------------------+
//| parametros                                                       |
//+------------------------------------------------------------------+
input double BALANCE=10000.0;
input double AMOUNT=10.0;
input double PAYOUT=0.50;

//+------------------------------------------------------------------+
//| dados internos                                                   |
//+------------------------------------------------------------------+
double BROKER_BALANCE = BALANCE;
double BROKER_LOT = AMOUNT;
double BROKER_PAYOUT = PAYOUT;
double USER_ORDER[] = { 0, 0, -1 };

//+------------------------------------------------------------------+
//| abre uma ordem ou troca (OP_BUY p/ compra ou OP_SELL p/ venda)   |
//+------------------------------------------------------------------+
bool OPEN_TRADE(int OP)
  {
   if (USER_ORDER[0] != 0 || USER_ORDER[1] != 0)
      return false; // Ja temos uma ordem em andamento

   if (BROKER_BALANCE < BROKER_LOT)
   {
      int diff = 0;
      diff = 1 / diff; // Para o advisor com uma excessao
      return false; // Balanco eh insuficiente
   }

   if(OP==OP_BUY || OP==OP_SELL)
     {
      USER_ORDER[0] = (int)TimeCurrent();  // Tempo atual
      USER_ORDER[1] = TRADE_PRICE();       // Preco atual
      USER_ORDER[2] = OP;                  // Tipo de trade
      BROKER_BALANCE -= BROKER_LOT;        // Atualizamos o balanco
      draw_a_line_from_trade();            // Desenhamos uma linha
      return true;
     }
   return false;
  }

//+------------------------------------------------------------------+
//| Descobre e retorna o preco atual                                 |
//+------------------------------------------------------------------+
double TRADE_PRICE()
  {
   return iClose(NULL, 0, 0);
  }

//+------------------------------------------------------------------+
//| Retorna uma string para se usada como nome do objeto linha       |
//+------------------------------------------------------------------+  
string get_object_name()
  {
   return "ACTUAL_ORDER";
  }

//+------------------------------------------------------------------+
//| Desenha uma linha para a trade atual                             |
//+------------------------------------------------------------------+  
void draw_a_line_from_trade()
  {
   int CHART_ID=0;
   string OBJ_NAME=get_object_name();
   if (ObjectFind(CHART_ID, OBJ_NAME) < 0)
     {
      ObjectCreate(CHART_ID, OBJ_NAME, OBJ_HLINE, 0, 0, USER_ORDER[1]);
      ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_BACK, false);
      ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_SELECTABLE, false);
      ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_SELECTED, false);
      ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_HIDDEN, true);
      ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_COLOR, (USER_ORDER[2] == OP_SELL ? clrRed : clrLime));
      ObjectSetInteger(CHART_ID, OBJ_NAME, OBJPROP_STYLE, STYLE_DASHDOT);
      string aux = (USER_ORDER[2] == OP_BUY ? "Buy" : "Sell") + " " + (string)ChartPeriod()+" Minutes";
      ObjectSetString(CHART_ID, OBJ_NAME, OBJPROP_TOOLTIP, aux);
     }
  }
  
//+------------------------------------------------------------------+
//| Encerra a trade, loga o resulta em um arquivo e remove a linha   |
//+------------------------------------------------------------------+
void CLOSE_TRADE()
  {
   int timeout = ExpireBarTimeout;
   
   if (USER_ORDER[0] == 0 || USER_ORDER[1] == 0)
      return ; // Nao temos uma trade

   if (TimeCurrent() < USER_ORDER[0] + (timeout * 60))
      return ; // Trade ainda nao expirou

   // Trade expirou!
   if (TRADE_PRICE() == USER_ORDER[1])
     {
      // Trade foi um empate! Devolvemos o investido
      BROKER_BALANCE += BROKER_LOT;
      log_a_tie();
     }
   else if (USER_ORDER[2] == OP_BUY)
     {
      if (TRADE_PRICE() > USER_ORDER[1])
        {
         // Preco foi maior que o valor apostado
         BROKER_BALANCE += BROKER_LOT + BROKER_LOT * BROKER_PAYOUT;
         log_a_win();
        }
      else log_a_loss();
     }
   else if (USER_ORDER[2] == OP_SELL)
     {
      if (TRADE_PRICE() < USER_ORDER[1])
        {
         // Price foi menor que o valor apostado
         BROKER_BALANCE += BROKER_LOT + BROKER_LOT * BROKER_PAYOUT;
         log_a_win();
        }
      else log_a_loss();
     }
   // Reiniciamos dados de trade internos
   USER_ORDER[0] = USER_ORDER[1] = 0;
   USER_ORDER[2] = -1;
   delete_trade_line();
  }

//+------------------------------------------------------------------+
//| Remove a linha desenhada de trade                                |
//+------------------------------------------------------------------+  
void delete_trade_line()
  {
   int CHART_ID = 0;
   string OBJ_NAME = get_object_name();
   if (ObjectFind(CHART_ID, OBJ_NAME) >= 0)
     ObjectDelete(CHART_ID,OBJ_NAME);
  }
  
//+------------------------------------------------------------------+
//| Chama a funcao de log quando houve um empate                     |
//+------------------------------------------------------------------+
void log_a_tie()
  {
   WriteData("TIE");
  }
  
//+------------------------------------------------------------------+
//| Chama a funcao de log quando houve uma vitoria                   |
//+------------------------------------------------------------------+
void log_a_win()
  {
   WriteData("WIN");
  }
  
//+------------------------------------------------------------------+
//| Chama a funcao de log quando houve uma perda                     |
//+------------------------------------------------------------------+
void log_a_loss()
  {
   WriteData("LOSS");
  }
  
//+------------------------------------------------------------------+
//| Abre e insere no final do arquivo os dados novos                 |
//+------------------------------------------------------------------+
void WriteData(string mode)
  {
     if (StringLen(FilenameLogTrades) == 0)
       return ; // User not defined a filename to log file
   ResetLastError();
   int file_handle=FileOpen("Data//"+FilenameLogTrades, FILE_READ|FILE_WRITE|FILE_CSV);
   if (file_handle==INVALID_HANDLE)
     return ; // Erro abrindo arquivo Data//FilenameLogTrades
   FileSeek(file_handle, 0, SEEK_END);
   if (FileIsEnding(file_handle))
     {
      FileWrite(file_handle, mode, ExpireBarTimeout, USER_ORDER[0], DoubleToStr(TRADE_PRICE(), 4),
                             USER_ORDER[1], USER_ORDER[2], DoubleToStr(BROKER_BALANCE, 4));
     }
   FileClose(file_handle);
  }
