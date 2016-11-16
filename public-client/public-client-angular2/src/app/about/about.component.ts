import { Component, OnInit } from '@angular/core';
import { StackItem } from './about.model'

@Component({
  selector: 'my-about',
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.scss']
})
export class AboutComponent implements OnInit {

    stackItems: StackItem[];

    constructor() {
        this.initStackItems();
    }

    ngOnInit() {
        //console.log('Hello About');
    }

    private initStackItems(): void {
        this.stackItems = [
            new StackItem(
                "Angular 2",
                "Angular 2 is used as the client side application framework.",
                "/img/angular.png"),
            new StackItem(
                "Bootstrap",
                "Bootstrap enables the mobile-first design through its responsive grid and components.",
                "/img/bootstrap.jpg"),
            new StackItem(
                "Python 3.5",
                "Python is used to develop server-side code including the API that backs the Angular app.",
                "/img/python.png"),
            new StackItem(
                "Flask",
                "Flask is used to implement server-side APIs and any server-side web applications.",
                "/img/flask.png"),
            new StackItem(
                "Redis",
                "Redis is used for fast, scalable data persistence and session management.",
                "/img/redis.png"),
            new StackItem(
                "CoreOS Dex",
                "Dex is a lightweight, standards-compliant OpenId Connect / OAuth 2 identity provider written in Go lang.",
                "/img/dex.jpg"),
            new StackItem(
                "Alpine Linux + Docker",
                "Docker is used to containerize all solution components as containers running the ultrasmall and fast Alpine Linux distribution.",
                "/img/alpine_docker.png")
            ];
    }

}
