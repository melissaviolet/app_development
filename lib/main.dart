import 'package:flutter/material.dart';

void main() => runApp(MaterialApp(home: WhatsApp()));

class WhatsApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.black87,
        title: Text(
          "WhatsApp",
          style: TextStyle(
            color:Colors.white,
            fontSize:40,
            fontWeight:FontWeight.bold,
          ),
        ),
        actions: [
          IconButton(
            icon: Icon(Icons.search),
            color: Colors.white,
            onPressed: () {
              
            },
          
          ),
          IconButton(
            icon: Icon(Icons.camera_alt),
            color: Colors.white,
            onPressed: () {
            },
          ),
          IconButton(
            icon: Icon(Icons.more_vert),
            color: Colors.white,
            onPressed: () {
            },
          ),

        ],
      ),
    );

  }
}
