import 'package:flutter/material.dart';
import 'quotes.dart';

class QuoteList extends StatefulWidget {
  //const QuoteList({super.key});

  @override
  _QuoteListState createState() => _QuoteListState();
}

class _QuoteListState extends State<QuoteList> {
  List<Quote> quotes = [
    Quote(text: "You are more than enough.", author: "Oscar wild"),
    Quote(text: "You are loved and cherished", author: "Blue Ivy"),
    Quote(text: "You must be earned", author: "Shuga"),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        title: Text("Amazing Quotes"),
        centerTitle: true,
        backgroundColor: Colors.cyan[200],
      ),

      body: Column(
        children: quotes.map((quote) {
          return Text('${quote.text} - ${quote.author}');
        }).toList(),
      ),
    );
  }
}
