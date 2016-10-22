import { Component, OnInit } from '@angular/core';
import { GuestbookEntry, GuestbookEntrySet } from '../../shared/api.model';
import { ApiService } from '../../shared/api.service';

@Component({
    selector: 'browse-guestbook',
    templateUrl: 'browse-guestbook.component.html',
    styleUrls: ['./browse-guestbook.component.scss']
})
export class BrowseGuestbookComponent implements OnInit {
    model: GuestbookEntry[];
    last_id: string;
    state_loaded: boolean;
    state_loading_more: boolean;
    state_has_more: boolean;

    constructor(private api: ApiService) {
        this.resetState();
        this.resetModel();
    }

    ngOnInit() {
        console.log('Loading guestbook');
        this.load();
    }

    load(): void {
        this.observeLoad();
    }

    observeLoad(): void {
        this.api.browseGuestbook()
            .subscribe(
                results => this.handleLoadComplete(results),
                error => console.error('Error: ' + error)
            );
    }

    private handleLoadComplete(results: GuestbookEntrySet): void {
        this.resetModel();
        if (results.count > 0) {
            this.fixResults(results);
            this.model = this.model.concat(results.entries);
            this.last_id = results.last_id
        }
        this.state_loaded = true;
        this.state_has_more = results.has_more;
        console.log('Loaded: '+JSON.stringify(results));
    }

    private fixResults(results: GuestbookEntrySet): void {
        for (let entry of results.entries) {
            if (entry.timestamp) entry.timestamp = new Date(entry.timestamp);
        }
    }

    loadMore() {
        this.state_loading_more = true;
        this.observeLoadMore();
    }

    observeLoadMore(): void {
        this.api.browseGuestbookMore(this.last_id)
            .subscribe(
                results => this.handleLoadMoreComplete(results),
                error => console.error('Error: ' + error)
            );
    }

    private handleLoadMoreComplete(results: GuestbookEntrySet): void {
        this.state_loading_more = false;
        if (results.count > 0) {
            this.fixResults(results);
            this.model = this.model.concat(results.entries);
            this.last_id = results.last_id
        }
        this.state_has_more = results.has_more;
    }

    resetState(): void {
        this.state_loaded = false;
        this.state_loading_more = false;
        this.state_has_more = false;
    }

    resetModel(): void {
        this.model = [];
    }

    // TODO: Remove this when we're done
    get diagnostic() { return JSON.stringify(this.model) + ' && state_loaded: ' + this.state_loaded + ' && state_loading_more: ' + this.state_loading_more; }
}