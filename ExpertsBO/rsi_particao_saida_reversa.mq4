//+------------------------------------------------------------------+
//|                                                 rsi_particao.mq4 |
//|                                                    Ricardo Lucca |
//|                                        http://github.com/~rlucca |
//+------------------------------------------------------------------+
#property copyright "Ricardo Lucca"
#property link      "http://github.com/~rlucca"
#property version   "1.00"
#property strict
//+------------------------------------------------------------------+
//| Parametros                                                       |
//+------------------------------------------------------------------+
input int InpPeriodRSI=14;
input double InpUpperLimit = 80;
input double InpLowerLimit = 20;

//+------------------------------------------------------------------+
//| Dados internos                                                   |
//+------------------------------------------------------------------+
int ExpireBarTimeout=Period();
int next_bar_trade=-1;
int prev_bars=0;

//+------------------------------------------------------------------+
//| Includes                                                         |
//+------------------------------------------------------------------+
#include <BinaryOptionTrade.mqh>
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
   CLOSE_TRADE();
   if(USER_ORDER[0]==0 && USER_ORDER[1]==0)
     {
      NEW_ORDER();
     }
  }
//+------------------------------------------------------------------+
//| Função que analisa e envia a ordem a ser executada               |
//+------------------------------------------------------------------+
void NEW_ORDER()
  {
   if(next_bar_trade!=-1)
     {
      if(Bars<=prev_bars)
         return;
      int bar_trade=get_trend();
      if(bar_trade!=-1 && next_bar_trade!=bar_trade)
         OPEN_TRADE(bar_trade);
      next_bar_trade=-1;
      return;
     }
   next_bar_trade=get_order_type();
   prev_bars=Bars;
  }
//+------------------------------------------------------------------+
//| Função que devolve a direcao na ordem a ser criada               |
//+------------------------------------------------------------------+
int get_order_type()
  {
   double prev_value=iRSI(NULL,0,InpPeriodRSI,PRICE_CLOSE,1);
   double curr_value=iRSI(NULL,0,InpPeriodRSI,PRICE_CLOSE,0);
   if(prev_value>InpUpperLimit && curr_value<InpUpperLimit)
     {
      return OP_SELL;
     }
   else if(prev_value<InpLowerLimit && curr_value>InpLowerLimit)
     {
      return OP_BUY;
     }
   return -1;
  }
//+------------------------------------------------------------------+
//| Função que devolve a direcao no movimento do RSI                 |
//+------------------------------------------------------------------+
int get_trend()
  {
   double prev_value=iRSI(NULL,0,InpPeriodRSI,PRICE_CLOSE,1);
   double curr_value=iRSI(NULL,0,InpPeriodRSI,PRICE_CLOSE,0);
   if(prev_value>curr_value)
      return OP_SELL;
   else if(prev_value<curr_value)
      return OP_BUY;
   return -1;
  }
//+------------------------------------------------------------------+
//| Função que devolve o nome do arquivo de log da execucao          |
//+------------------------------------------------------------------+
string FilenameLogTrades()
  {
   string filename="rsi_particao_saida_reversa_";
   filename += IntegerToString(InpPeriodRSI) + "_";
   filename += DoubleToStr(InpLowerLimit, 0) + "_";
   filename += DoubleToStr(InpUpperLimit, 0);
   return filename + ".csv";
  }
//+------------------------------------------------------------------+
