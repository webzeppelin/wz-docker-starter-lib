import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'my-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

    active_view: string;

    constructor(private router: Router, private route: ActivatedRoute) {
        // this.active_view = "sign";
    }

    clickSign(): void {
        this.router.navigate(['/sign']);
    }

    clickBrowse(): void {
        this.router.navigate(['/browse']);
    }

    clickSearch(): void {
        this.router.navigate(['/search']);
    }

    private setActiveViewFromRoute(): void {
        let path_segs = this.route.snapshot.url;
        if (path_segs.length > 0) {
            this.setActiveView(path_segs[path_segs.length-1].path);
        }
        console.log('ActiveView = '+this.active_view);
    }

    ngOnInit() {
        this.setActiveViewFromRoute();
    }

    setActiveView(av: string): void {
        this.active_view = av;
    }
}
